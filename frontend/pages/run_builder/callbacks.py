"""Callbacks for Run Builder page."""

import copy
from dash import ALL, callback, ctx, html, Input, no_update, Output, State
from dash.exceptions import PreventUpdate
from loguru import logger
import dash_bootstrap_components as dbc

from components.resource_form import render_resource_form
from utilities import api
from utilities.normalizers import normalize_values
from utilities.payload_builder import build_payload
from utilities.resource_helpers import get_user_friendly_message

from pages.run_builder.config import (
    RESOURCES,
    SCENARIO_CHILD_RESOURCES,
    agentconfig_fields,
    prevention_fields,
    scenario_fields,
    simulation_fields,
    virus_fields,
)

from pages.run_builder.layout import render_summary_view


@callback(
    Output('scenario-builder-how-to-modal', 'is_open'),
    [Input('scenario-builder-how-to-btn', 'n_clicks'), Input('scenario-builder-how-to-close', 'n_clicks')],
    [State('scenario-builder-how-to-modal', 'is_open')],
    prevent_initial_call=True,
)
def toggle_how_to_modal(n1, n2, is_open):
    """Toggle how-to modal."""
    return not is_open


@callback(
    Output('scenario-agent-completion-store', 'data'),
    [
        Input({'type': 'dropdown', 'resource': 'scenario'}, 'value'),
        Input({'type': 'dropdown', 'resource': 'agent_config'}, 'value'),
    ],
    State('scenario-agent-completion-store', 'data'),
)
def track_scenario_agent_completion(scenario_value, agent_value, completion_data):
    """Track when both scenario and agent config are selected or created."""
    completion_data = completion_data or {'scenario_ready': False, 'agent_ready': False}

    completion_data['scenario_ready'] = scenario_value is not None
    completion_data['agent_ready'] = agent_value is not None

    return completion_data


@callback(
    Output('scenario-agent-completion-modal', 'is_open'),
    [
        Input('scenario-agent-completion-store', 'data'),
        Input('completion-keep-editing-btn', 'n_clicks'),
    ],
    State('scenario-agent-completion-modal', 'is_open'),
    prevent_initial_call=True,
)
def show_completion_modal(completion_data, keep_editing_clicks, is_open):
    """Show modal when both scenario and agent are ready."""
    triggered_id = ctx.triggered_id

    # Close modal if keep editing is clicked
    if triggered_id == 'completion-keep-editing-btn':
        return False

    # Open modal if both are ready and modal is not already open
    if completion_data and completion_data.get('scenario_ready') and completion_data.get('agent_ready'):
        if not is_open:
            return True

    return is_open


def extract_resource_id(value):
    """Return an id from either a raw value or mapping."""
    if isinstance(value, dict):
        return value.get('id') or value.get('value') or value.get('name')
    return value


@callback(
    [
        Output({'type': 'dropdown', 'resource': 'virus'}, 'value', allow_duplicate=True),
        Output({'type': 'dropdown', 'resource': 'prevention'}, 'value', allow_duplicate=True),
        Output({'type': 'dropdown', 'resource': 'simulation'}, 'value', allow_duplicate=True),
    ],
    Input({'type': 'original-data', 'resource': 'scenario'}, 'data'),
    State({'type': 'form-mode', 'resource': 'scenario'}, 'data'),
    prevent_initial_call='initial_duplicate',
)
def sync_child_dropdowns_from_scenario(scenario_data, scenario_mode):
    """Keep child dropdown selections in sync with the selected scenario only when editing."""
    if not scenario_data:
        return None, None, None

    # Only sync child dropdowns when actively editing a scenario
    mode_data = scenario_mode or {}
    mode = mode_data.get('mode', 'idle')
    editing = mode_data.get('editing', False)

    if mode != 'edit' or not editing:
        return None, None, None

    virus_id = extract_resource_id(scenario_data.get('virus') or scenario_data.get('virus_id'))
    prevention_id = extract_resource_id(scenario_data.get('prevention') or scenario_data.get('prevention_id'))
    sim_id = extract_resource_id(
        scenario_data.get('sim') or scenario_data.get('simulation') or scenario_data.get('simulation_id')
    )
    return virus_id, prevention_id, sim_id


@callback(
    [
        *[Output({'type': 'form-mode', 'resource': r}, 'data', allow_duplicate=True) for r in SCENARIO_CHILD_RESOURCES],
        *[
            Output({'type': 'original-data', 'resource': r}, 'data', allow_duplicate=True)
            for r in SCENARIO_CHILD_RESOURCES
        ],
        *[
            Output({'type': 'resource-store', 'resource': r}, 'data', allow_duplicate=True)
            for r in SCENARIO_CHILD_RESOURCES
        ],
        *[Output({'type': 'dropdown', 'resource': r}, 'value', allow_duplicate=True) for r in SCENARIO_CHILD_RESOURCES],
    ],
    Input({'type': 'form-mode', 'resource': 'scenario'}, 'data'),
    prevent_initial_call='initial_duplicate',
)
def reset_children_when_scenario_resets(scenario_mode):
    """Return child sections to idle/blank when scenario is idle, in summary mode, or creating new."""
    if not scenario_mode:
        form_modes = [{'mode': 'idle', 'resource_id': None} for _ in SCENARIO_CHILD_RESOURCES]
        originals = [None for _ in SCENARIO_CHILD_RESOURCES]
        stores = [None for _ in SCENARIO_CHILD_RESOURCES]
        dropdowns = [None for _ in SCENARIO_CHILD_RESOURCES]
        return tuple(form_modes + originals + stores + dropdowns)

    mode = scenario_mode.get('mode')
    editing = scenario_mode.get('editing', False)

    # Keep children idle unless we're actively editing a scenario
    if mode == 'idle' or mode == 'summary' or (mode == 'edit' and not editing):
        form_modes = [{'mode': 'idle', 'resource_id': None} for _ in SCENARIO_CHILD_RESOURCES]
        originals = [None for _ in SCENARIO_CHILD_RESOURCES]
        stores = [None for _ in SCENARIO_CHILD_RESOURCES]
        dropdowns = [None for _ in SCENARIO_CHILD_RESOURCES]
        return tuple(form_modes + originals + stores + dropdowns)

    return (no_update,) * (len(SCENARIO_CHILD_RESOURCES) * 4)


@callback(
    Output('scenario-child-tabs', 'style'),
    Output('scenario-action-buttons', 'style'),
    Input({'type': 'form-mode', 'resource': 'scenario'}, 'data'),
    Input({'type': 'dropdown', 'resource': 'scenario'}, 'value'),
    prevent_initial_call=False,
)
def toggle_child_tabs(scenario_mode, _scenario_selected):
    """Show child config tabs (and scenario save/cancel) only when creating/editing a scenario."""
    data = scenario_mode or {}
    mode = data.get('mode', 'idle')
    editing = data.get('editing', False)
    if mode == 'edit' and editing:
        return {'display': 'block'}, {'display': 'flex'}
    return {'display': 'none'}, {'display': 'none'}


def register_form_renderer(resource_type, fields):
    """Register a form rendering callback for a resource."""

    @callback(
        Output(f'{resource_type}-editable-fields', 'children'),
        [
            Input({'type': 'form-mode', 'resource': resource_type}, 'data'),
            Input({'type': 'original-data', 'resource': resource_type}, 'data'),
        ],
        prevent_initial_call=False,
    )
    def render_form(mode_data, values_data):
        mode = (mode_data or {}).get('mode', 'idle')
        clean = normalize_values(resource_type, values_data)

        if mode == 'edit':
            form = render_resource_form(resource_type, fields, values=clean, readonly=False)
            if resource_type == 'scenario':
                return html.Div([form])

            return html.Div(
                [
                    form,
                    html.Div(
                        [
                            html.Button('Save', id=f'{resource_type}-save-btn', className='btn btn-primary'),
                            html.Button(
                                'Cancel', id=f'{resource_type}-cancel-btn-bottom', className='btn btn-secondary'
                            ),
                        ],
                        className='form-button-group',
                    ),
                ]
            )

        if mode == 'summary' and values_data:
            summary = render_summary_view(resource_type, clean or values_data)
            return html.Div(
                [
                    summary,
                    html.Div(
                        [
                            html.Button(
                                [
                                    html.I(className='fa fa-check-circle me-2'),
                                    'Confirm',
                                ],
                                id={'type': 'select-btn', 'resource': resource_type},
                                className='btn btn-success btn-action',
                            ),
                            html.Button(
                                [
                                    html.I(className='fa fa-pen-to-square me-2'),
                                    'Edit',
                                ],
                                id={'type': 'edit-btn', 'resource': resource_type},
                                className='btn btn-primary btn-action',
                            ),
                            html.Button(
                                [
                                    html.I(className='fa fa-copy me-2'),
                                    'Duplicate',
                                ],
                                id={'type': 'clone-btn', 'resource': resource_type},
                                className='btn btn-info btn-action',
                            ),
                            html.Button(
                                [
                                    html.I(className='fa fa-trash-can me-2'),
                                    'Remove',
                                ],
                                id={'type': 'delete-btn', 'resource': resource_type},
                                className='btn btn-danger btn-action',
                            ),
                        ],
                        className='form-button-group-single-row',
                    ),
                ]
            )
        if mode == 'idle':
            return html.Div()

        return html.Div()


@callback(
    [Output({'type': 'dropdown', 'resource': ALL}, 'options')], [Input({'type': 'dropdown', 'resource': ALL}, 'id')]
)
def populate_dropdowns(dropdown_ids):
    """Populate all dropdowns from API."""
    return [
        [
            [{'label': r['name'], 'value': r['id']} for r in resources]
            if (success := api.get_all(d['resource']))[0] and (resources := success[1])
            else []
            for d in dropdown_ids
        ]
    ]


def register_modal_loader(resource):
    """Load a resource from dropdown selection and show summary inline."""
    # Child resources need to check scenario mode
    if resource in SCENARIO_CHILD_RESOURCES:

        @callback(
            Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
            Output({'type': 'original-data', 'resource': resource}, 'data', allow_duplicate=True),
            Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
            Input({'type': 'dropdown', 'resource': resource}, 'value'),
            State({'type': 'form-mode', 'resource': 'scenario'}, 'data'),
            State({'type': 'form-mode', 'resource': resource}, 'data'),
            prevent_initial_call=True,
        )
        def _load_selection(selected_id, scenario_mode, current_mode):
            # If dropdown cleared but we're in edit mode (creating new), don't reset
            if not selected_id:
                if current_mode and current_mode.get('mode') == 'edit':
                    raise PreventUpdate
                return None, None, {'mode': 'idle', 'resource_id': None}

            # Only allow child resource loading when actively editing a scenario
            scenario_data = scenario_mode or {}
            mode = scenario_data.get('mode', 'idle')
            editing = scenario_data.get('editing', False)

            if mode != 'edit' or not editing:
                raise PreventUpdate

            success, item, _ = api.get_by_id(resource, selected_id)
            if not success:
                raise PreventUpdate

            mode_payload = {'mode': 'summary', 'resource_id': selected_id}
            return selected_id, item, mode_payload
    else:

        @callback(
            Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
            Output({'type': 'original-data', 'resource': resource}, 'data', allow_duplicate=True),
            Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
            Input({'type': 'dropdown', 'resource': resource}, 'value'),
            State({'type': 'form-mode', 'resource': resource}, 'data'),
            prevent_initial_call=True,
        )
        def _load_selection(selected_id, current_mode):
            # If dropdown cleared but we're in edit mode (creating new), don't reset
            if not selected_id:
                if current_mode and current_mode.get('mode') == 'edit':
                    raise PreventUpdate
                mode_payload = {'mode': 'idle', 'resource_id': None}
                if resource == 'scenario':
                    mode_payload['editing'] = False
                return None, None, mode_payload

            success, item, _ = api.get_by_id(resource, selected_id)
            if not success:
                raise PreventUpdate

            mode_payload = {'mode': 'summary', 'resource_id': selected_id}
            if resource == 'scenario':
                mode_payload['editing'] = False

            return selected_id, item, mode_payload


def register_create(resource):
    """Register a create callback for a resource."""

    @callback(
        Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'original-data', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'dropdown', 'resource': resource}, 'value', allow_duplicate=True),
        Input({'type': 'create-btn', 'resource': resource}, 'n_clicks'),
        prevent_initial_call=True,
    )
    def _create(_n):
        mode_payload = {'mode': 'edit', 'resource_id': None}
        if resource == 'scenario':
            mode_payload['editing'] = True  # Show child tabs when creating new scenario

        return mode_payload, {}, None, None


def register_edit_clone(resource):
    """Register an edit and clone callback for a resource."""

    @callback(
        Output({'type': 'original-data', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
        Input({'type': 'edit-btn', 'resource': resource}, 'n_clicks'),
        Input({'type': 'clone-btn', 'resource': resource}, 'n_clicks'),
        State({'type': 'resource-store', 'resource': resource}, 'data'),
        prevent_initial_call=True,
    )
    def _edit_clone(_edit, _clone, stored_id):
        # Prevent firing when buttons are first rendered (n_clicks is None)
        if not _edit and not _clone:
            raise PreventUpdate

        if not ctx.triggered_id:
            raise PreventUpdate

        is_clone = ctx.triggered_id['type'] == 'clone-btn'
        success, item, _ = api.get_by_id(resource, stored_id)

        if not success:
            raise PreventUpdate

        item = copy.deepcopy(item)
        if is_clone:
            item.pop('id', None)
            item['name'] = f'{item["name"]}-copy'
            stored_id = None

        mode_payload = {'mode': 'edit', 'resource_id': stored_id}
        if resource == 'scenario':
            mode_payload['editing'] = True  # Show child tabs when editing/cloning existing scenario

        return item, mode_payload, stored_id


def register_delete(resource):
    """Register a delete callback for a resource - shows confirmation modal."""

    @callback(
        Output('delete-confirmation-modal', 'is_open', allow_duplicate=True),
        Output('delete-confirmation-message', 'children', allow_duplicate=True),
        Output('delete-pending-resource', 'data', allow_duplicate=True),
        Output('delete-pending-id', 'data', allow_duplicate=True),
        Input({'type': 'delete-btn', 'resource': resource}, 'n_clicks'),
        State({'type': 'resource-store', 'resource': resource}, 'data'),
        State({'type': 'original-data', 'resource': resource}, 'data'),
        prevent_initial_call=True,
    )
    def _show_delete_confirmation(n, stored_id, item_data):
        if not n or not stored_id:
            raise PreventUpdate

        # Get item name for confirmation message
        item_name = item_data.get('name', 'this item') if item_data else 'this item'
        resource_labels = {
            'scenario': 'scenario',
            'simulation': 'simulation configuration',
            'virus': 'virus parameters',
            'prevention': 'prevention measures',
            'agent_config': 'agent configuration',
        }
        label = resource_labels.get(resource, resource)

        message = f'Are you sure you want to delete the {label} "{item_name}"? This action cannot be undone.'

        return True, message, resource, stored_id


def register_confirm(resource):
    """Register a confirm/select callback for a resource selection."""

    @callback(
        Output({'type': 'dropdown', 'resource': resource}, 'value', allow_duplicate=True),
        Output('notification-message-store', 'data', allow_duplicate=True),
        Output('notification-type-store', 'data', allow_duplicate=True),
        Input({'type': 'select-btn', 'resource': resource}, 'n_clicks'),
        State({'type': 'resource-store', 'resource': resource}, 'data'),
        prevent_initial_call=True,
    )
    def _confirm(n, stored_id):
        if not n:
            raise PreventUpdate
        message = get_user_friendly_message(resource, 'select', True)
        return stored_id, message, 'success'


def register_cancel(resource):
    """Register a cancel callback for a resource form."""

    @callback(
        Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'original-data', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'dropdown', 'resource': resource}, 'value', allow_duplicate=True),
        Input(f'{resource}-cancel-btn-bottom', 'n_clicks'),
        prevent_initial_call=True,
    )
    def _cancel(n):
        if not n:
            raise PreventUpdate
        # Return to initial state with no selection
        return {'mode': 'idle', 'resource_id': None}, None, None, None


def register_save(resource):
    """Register a save callback for a resource."""
    extra_states = []
    if resource == 'prevention':
        extra_states = [
            State({'type': 'mask-effectiveness-slider', 'mask': ALL}, 'value'),
            State({'type': 'mask-effectiveness-slider', 'mask': ALL}, 'id'),
            State({'type': 'mask-checkbox', 'mask': ALL}, 'value'),
            State({'type': 'mask-checkbox', 'mask': ALL}, 'id'),
            State({'type': 'vaccine-dose', 'vaccine': ALL, 'dose': ALL}, 'value'),
            State({'type': 'vaccine-dose', 'vaccine': ALL, 'dose': ALL}, 'id'),
            State({'type': 'vaccine-checkbox', 'vaccine': ALL}, 'value'),
            State({'type': 'vaccine-checkbox', 'vaccine': ALL}, 'id'),
        ]
    if resource == 'scenario':
        extra_states = [
            State({'type': 'dropdown', 'resource': 'virus'}, 'value'),
            State({'type': 'dropdown', 'resource': 'prevention'}, 'value'),
            State({'type': 'dropdown', 'resource': 'simulation'}, 'value'),
        ]

    @callback(
        Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'dropdown', 'resource': resource}, 'value', allow_duplicate=True),
        Output({'type': 'dropdown', 'resource': resource}, 'options', allow_duplicate=True),
        Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'original-data', 'resource': resource}, 'data', allow_duplicate=True),
        Output('notification-message-store', 'data', allow_duplicate=True),
        Output('notification-type-store', 'data', allow_duplicate=True),
        Input(f'{resource}-save-btn', 'n_clicks'),
        State({'type': 'form-input', 'resource': resource, 'field': ALL}, 'value'),
        State({'type': 'form-input', 'resource': resource, 'field': ALL}, 'id'),
        State({'type': 'form-mode', 'resource': resource}, 'data'),
        State({'type': 'original-data', 'resource': resource}, 'data'),
        *extra_states,
        prevent_initial_call=True,
    )
    def _save(n, values, ids, mode, original, *extras):
        if not n:
            raise PreventUpdate
        form_data = {input_id['field']: value for input_id, value in zip(ids, values)}

        extras_map = {}
        if resource == 'prevention' and extras:
            (
                mask_values,
                mask_ids,
                mask_checks,
                mask_check_ids,
                vaccine_dose_values,
                vaccine_dose_ids,
                vaccine_checks,
                vaccine_check_ids,
            ) = extras

            selected_masks = {
                chk_id.get('mask')
                for chk_id, chk_val in zip(mask_check_ids, mask_checks)
                if chk_val and chk_id.get('mask') in chk_val
            }
            mask_payload = {
                m_id.get('mask'): (float(m_val) if m_id.get('mask') in selected_masks else 0.0)
                for m_id, m_val in zip(mask_ids, mask_values)
                if isinstance(m_id, dict)
            }

            selected_vax = {
                chk_id.get('vaccine')
                for chk_id, chk_val in zip(vaccine_check_ids, vaccine_checks)
                if chk_val and chk_id.get('vaccine') in chk_val
            }
            vax_payload = {}
            for v_id, v_val in zip(vaccine_dose_ids, vaccine_dose_values):
                if not isinstance(v_id, dict):
                    continue
                v_type, dose_idx = v_id.get('vaccine'), (v_id.get('dose') or 1) - 1
                doses = vax_payload.setdefault(v_type, [0.0, 0.0, 0.0])
                if v_type and 0 <= dose_idx < 3:
                    doses[dose_idx] = float(v_val) if v_type in selected_vax else 0.0

            for v_type in selected_vax:
                vax_payload.setdefault(v_type, [0.0, 0.0, 0.0])

            extras_map = {'mask': mask_payload, 'vax': vax_payload}
        elif resource == 'scenario' and extras:
            virus_id, prevention_id, simulation_id = extras
            form_data['virus'] = virus_id
            form_data['prevention'] = prevention_id
            form_data['sim'] = simulation_id

        payload = build_payload(resource, form_data, original, extras_map)

        logger.debug(f'\n=== SAVE {resource.upper()} ===')
        logger.debug('Payload:', form_data)
        logger.debug(f'Final Payload Sent to API: {payload}')

        rid = mode.get('resource_id')

        if rid:
            success, item, err = api.update(resource, rid, payload)
        else:
            success, item, err = api.create(resource, payload)

        action = 'update' if rid else 'create'

        if not success:
            message = get_user_friendly_message(resource, action, False, err)
            return no_update, no_update, no_update, no_update, no_update, message, 'error'

        new_id = item['id']
        message = get_user_friendly_message(resource, action, True)

        success_all, resources, _ = api.get_all(resource)
        opts = [{'label': r['name'], 'value': r['id']} for r in resources] if success_all and resources else []

        return {'mode': 'summary', 'resource_id': new_id}, new_id, opts, new_id, item, message, 'success'


@callback(
    Output('delete-confirmation-modal', 'is_open', allow_duplicate=True),
    Output({'type': 'dropdown', 'resource': ALL}, 'value', allow_duplicate=True),
    Output({'type': 'dropdown', 'resource': ALL}, 'options', allow_duplicate=True),
    Output({'type': 'resource-store', 'resource': ALL}, 'data', allow_duplicate=True),
    Output({'type': 'original-data', 'resource': ALL}, 'data', allow_duplicate=True),
    Output({'type': 'form-mode', 'resource': ALL}, 'data', allow_duplicate=True),
    Output('notification-message-store', 'data', allow_duplicate=True),
    Output('notification-type-store', 'data', allow_duplicate=True),
    Input('confirm-delete-btn', 'n_clicks'),
    Input('cancel-delete-btn', 'n_clicks'),
    State('delete-pending-resource', 'data'),
    State('delete-pending-id', 'data'),
    State({'type': 'dropdown', 'resource': ALL}, 'id'),
    prevent_initial_call=True,
)
def handle_delete_confirmation(_confirm_clicks, _cancel_clicks, pending_resource, pending_id, dropdown_ids):
    """Handle the actual delete after confirmation or cancel."""
    if not ctx.triggered_id:
        raise PreventUpdate

    if ctx.triggered_id == 'cancel-delete-btn':
        return False, *[no_update] * (len(dropdown_ids) * 5 + 2)

    if ctx.triggered_id == 'confirm-delete-btn' and pending_resource and pending_id:
        success, _, err = api.delete(pending_resource, pending_id)

        message = get_user_friendly_message(pending_resource, 'delete', success, err)
        notification_type = 'success' if success else 'error'

        # Prepare outputs for all resources
        dropdown_values = []
        dropdown_options = []
        store_values = []
        original_values = []
        mode_values = []

        for dropdown_id in dropdown_ids:
            res = dropdown_id['resource']
            if res == pending_resource and success:
                # Update the deleted resource's dropdown
                success_all, resources, _ = api.get_all(res)
                opts = [{'label': r['name'], 'value': r['id']} for r in resources] if success_all and resources else []

                dropdown_values.append(None)
                dropdown_options.append(opts)
                store_values.append(None)
                original_values.append(None)

                mode_payload = {'mode': 'idle', 'resource_id': None}
                if res == 'scenario':
                    mode_payload['editing'] = False
                mode_values.append(mode_payload)
            else:
                # Keep other resources unchanged
                dropdown_values.append(no_update)
                dropdown_options.append(no_update)
                store_values.append(no_update)
                original_values.append(no_update)
                mode_values.append(no_update)

        return (
            False,
            dropdown_values,
            dropdown_options,
            store_values,
            original_values,
            mode_values,
            message,
            notification_type,
        )

    raise PreventUpdate


@callback(
    Output('notification-modal', 'is_open'),
    Output('notification-modal-title', 'children'),
    Output('notification-modal-body', 'children'),
    Output('notification-modal', 'className'),
    Input('notification-message-store', 'data'),
    Input('notification-type-store', 'data'),
    Input('close-notification-modal', 'n_clicks'),
    State('notification-modal', 'is_open'),
    prevent_initial_call=True,
)
def toggle_notification_modal(message, notification_type, _close_clicks, _is_open):
    """Open/close notification modal with appropriate message and styling."""
    triggered_id = ctx.triggered_id

    # Close button clicked
    if triggered_id == 'close-notification-modal':
        return False, no_update, no_update, no_update

    # New notification
    if message and notification_type:
        title = 'Success' if notification_type == 'success' else 'Error'
        modal_class = 'notification-success' if notification_type == 'success' else 'notification-error'
        return True, title, message, modal_class

    return no_update, no_update, no_update, no_update


@callback(
    Output('scenario-learn-more-modal', 'is_open'),
    Input('scenario-learn-more-btn', 'n_clicks'),
    Input('close-scenario-learn-more', 'n_clicks'),
    State('scenario-learn-more-modal', 'is_open'),
    prevent_initial_call=True,
)
def toggle_scenario_learn_more(open_clicks, close_clicks, is_open):
    """Toggle scenario learn more modal."""
    return not is_open


@callback(
    Output('agent-config-learn-more-modal', 'is_open'),
    Input('agent-config-learn-more-btn', 'n_clicks'),
    Input('close-agent-config-learn-more', 'n_clicks'),
    State('agent-config-learn-more-modal', 'is_open'),
    prevent_initial_call=True,
)
def toggle_agent_config_learn_more(open_clicks, close_clicks, is_open):
    """Toggle agent config learn more modal."""
    return not is_open


def register_all_callbacks():
    """Register all callbacks for resources."""
    # Register form renderers
    register_form_renderer('agent_config', agentconfig_fields)
    register_form_renderer('virus', virus_fields)
    register_form_renderer('prevention', prevention_fields)
    register_form_renderer('simulation', simulation_fields)
    register_form_renderer('scenario', scenario_fields)

    # Register CRUD callbacks for all resources
    for res in RESOURCES:
        register_create(res)
        register_edit_clone(res)
        register_delete(res)
        register_confirm(res)
        register_cancel(res)
        register_save(res)
        register_modal_loader(res)
