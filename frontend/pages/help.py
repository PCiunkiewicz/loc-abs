"""Help Page for LocABS Application."""

from dash import html, register_page, callback, Input, Output, State
import dash_bootstrap_components as dbc

register_page(__name__, path='/help', name='Help', title='LocABS · Help')

# FAQ Data Structure
FAQ_DATA = {
    'Getting Started': [
        {
            'question': 'How do I create my first simulation?',
            'answer': 'To create your first simulation, navigate to the Run Builder page. Start by selecting or creating a scenario in Step 1, then configure your participants in Step 2. Finally, review and launch your simulation in Step 3.',
        },
        {
            'question': 'What are the system requirements?',
            'answer': 'LocABS runs in a web browser and requires Docker for deployment. Recommended browsers include Chrome, Firefox, or Edge. For optimal performance, use a system with at least 8GB RAM.',
        },
        {
            'question': 'How do I access my simulation results?',
            'answer': 'Navigate to the Dashboard page to view all completed simulations. Click on any simulation to view detailed results, or use the Data Visualization page for advanced analytics.',
        },
    ],
    'Scenario Configuration': [
        {
            'question': 'What is a scenario?',
            'answer': 'A scenario represents a unique test condition that includes outbreak settings, protective measures, and simulation parameters. Each scenario can be reused across multiple simulation runs.',
        },
        {
            'question': 'How do I configure prevention measures?',
            'answer': 'In the Scenario Builder, navigate to the Protective Measures tab. Here you can configure masks, vaccines, social distancing policies, and other prevention strategies.',
        },
        {
            'question': 'Can I clone existing scenarios?',
            'answer': 'Yes! When viewing a scenario in the dropdown, click the "Clone" button to create a copy that you can modify without affecting the original.',
        },
    ],
    'Participant Configuration': [
        {
            'question': 'What are participant profiles?',
            'answer': 'Participant profiles define how individuals behave in the simulation, including movement patterns, social interactions, and compliance with protective measures.',
        },
        {
            'question': 'How many participants can I configure?',
            'answer': 'You can configure up to 20 different participant profiles, each representing a unique behavior pattern within your facility.',
        },
        {
            'question': 'What is the difference between population and profiles?',
            'answer': 'Population refers to the total number of individuals in the simulation, while profiles define the behavior categories. Multiple individuals can share the same profile.',
        },
    ],
    'Results & Analysis': [
        {
            'question': 'How do I interpret simulation results?',
            'answer': 'The Dashboard provides key metrics including infection rates, duration, and status. Use the Data Visualization page for detailed charts and graphs showing transmission patterns over time.',
        },
        {
            'question': 'Can I export my results?',
            'answer': 'Yes! Navigate to the Data Visualization page and use the export functionality to download your simulation results in various formats.',
        },
        {
            'question': 'How long are results stored?',
            'answer': 'Simulation results are stored permanently in the database unless manually deleted. You can access historical runs at any time through the Dashboard.',
        },
    ],
}


def create_faq_accordion(topic, faqs, topic_id):
    """Create an accordion component for FAQ items."""
    accordion_items = []

    for idx, faq in enumerate(faqs):
        accordion_items.append(
            dbc.AccordionItem(
                html.P(faq['answer'], className='help-faq-answer'),
                title=faq['question'],
                item_id=f'{topic_id}-{idx}',
            )
        )

    return dbc.Accordion(
        accordion_items,
        id=f'accordion-{topic_id}',
        start_collapsed=True,
        always_open=True,
        className='help-accordion',
    )


layout = html.Div(
    [
        # Top Action Buttons
        html.Div(
            [
                html.Button(
                    [html.I(className='fa fa-rocket me-2'), 'GETTING STARTED'],
                    id='help-getting-started-btn',
                    className='btn btn-outline-dark help-action-btn',
                ),
                html.Button(
                    [html.I(className='fa fa-wrench me-2'), 'SCENARIO BUILDER'],
                    id='help-scenario-builder-btn',
                    className='btn btn-outline-dark help-action-btn',
                ),
                html.Button(
                    [html.I(className='fa fa-book me-2'), 'GLOSSARY TERMS'],
                    id='help-glossary-btn',
                    className='btn btn-outline-dark help-action-btn',
                ),
                html.Button(
                    [html.I(className='fa fa-headset me-2'), 'CONTACT SUPPORT'],
                    id='help-contact-btn',
                    className='btn btn-outline-dark help-action-btn',
                ),
            ],
            className='help-action-buttons',
        ),
        # Video Demo Section
        html.Div(
            [
                html.Div(
                    'VIDEO TUTORIALS & DEMOS',
                    className='help-video-header',
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.I(className='fa fa-play-circle help-video-icon'),
                                html.H5('Getting Started Tutorial', className='help-video-title'),
                                html.P(
                                    'Learn the basics of LocABS in this comprehensive walkthrough. '
                                    'This 10-minute tutorial covers scenario creation, participant configuration, and running your first simulation.',
                                    className='help-video-description',
                                ),
                                html.Button(
                                    [html.I(className='fa fa-play me-2'), 'Watch Tutorial'],
                                    className='btn btn-dark help-video-btn',
                                ),
                            ],
                            className='help-video-card',
                        ),
                        html.Div(
                            [
                                html.I(className='fa fa-chart-line help-video-icon'),
                                html.H5('Data Visualization Guide', className='help-video-title'),
                                html.P(
                                    'Discover how to analyze and visualize your simulation results. '
                                    'Learn to create charts, export data, and interpret key metrics from your runs.',
                                    className='help-video-description',
                                ),
                                html.Button(
                                    [html.I(className='fa fa-play me-2'), 'Watch Guide'],
                                    className='btn btn-dark help-video-btn',
                                ),
                            ],
                            className='help-video-card',
                        ),
                        html.Div(
                            [
                                html.I(className='fa fa-lightbulb help-video-icon'),
                                html.H5('Advanced Tips & Tricks', className='help-video-title'),
                                html.P(
                                    'Take your simulations to the next level with advanced features. '
                                    'Explore scenario optimization, batch processing, and decision support tools.',
                                    className='help-video-description',
                                ),
                                html.Button(
                                    [html.I(className='fa fa-play me-2'), 'Watch Tips'],
                                    className='btn btn-dark help-video-btn',
                                ),
                            ],
                            className='help-video-card',
                        ),
                    ],
                    className='help-video-grid',
                ),
            ],
            className='help-video-section',
        ),
        # FAQ Section
        html.Div(
            [
                # Top Row - Getting Started & Scenario Configuration
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    'FAQ: GETTING STARTED',
                                    className='help-section-header',
                                ),
                                html.Div(
                                    create_faq_accordion(
                                        'Getting Started', FAQ_DATA['Getting Started'], 'getting-started'
                                    ),
                                    className='help-section-content',
                                ),
                            ],
                            className='help-faq-section',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    'FAQ: SCENARIO CONFIGURATION',
                                    className='help-section-header',
                                ),
                                html.Div(
                                    create_faq_accordion(
                                        'Scenario Configuration', FAQ_DATA['Scenario Configuration'], 'scenario-config'
                                    ),
                                    className='help-section-content',
                                ),
                            ],
                            className='help-faq-section',
                        ),
                    ],
                    className='help-faq-row',
                ),
                # Bottom Row - Participant Configuration & Results
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    'FAQ: PARTICIPANT CONFIGURATION',
                                    className='help-section-header',
                                ),
                                html.Div(
                                    create_faq_accordion(
                                        'Participant Configuration',
                                        FAQ_DATA['Participant Configuration'],
                                        'participant-config',
                                    ),
                                    className='help-section-content',
                                ),
                            ],
                            className='help-faq-section',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    'FAQ: RESULTS & ANALYSIS',
                                    className='help-section-header',
                                ),
                                html.Div(
                                    create_faq_accordion(
                                        'Results & Analysis', FAQ_DATA['Results & Analysis'], 'results-analysis'
                                    ),
                                    className='help-section-content',
                                ),
                            ],
                            className='help-faq-section',
                        ),
                    ],
                    className='help-faq-row',
                ),
            ],
            className='help-faq-container',
        ),
        # Modals for action buttons
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle('Contact Support')),
                dbc.ModalBody(
                    [
                        html.P('Need help? Our support team is here to assist you.'),
                        html.Hr(),
                        html.Div(
                            [
                                html.P([html.Strong('Email: '), 'support@locabs.com']),
                                html.P(
                                    [html.Strong('Documentation: '), html.A('View Docs', href='#', target='_blank')]
                                ),
                                html.P(
                                    [html.Strong('GitHub Issues: '), html.A('Report a Bug', href='#', target='_blank')]
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.ModalFooter(dbc.Button('Close', id='close-contact-modal', className='btn btn-secondary')),
            ],
            id='contact-support-modal',
            is_open=False,
            centered=True,
        ),
    ],
    className='help-page-container',
)


# Callbacks
@callback(
    Output('contact-support-modal', 'is_open'),
    [Input('help-contact-btn', 'n_clicks'), Input('close-contact-modal', 'n_clicks')],
    [State('contact-support-modal', 'is_open')],
    prevent_initial_call=True,
)
def toggle_contact_modal(n1, n2, is_open):
    """Toggle contact support modal."""
    return not is_open
