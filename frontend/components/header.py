"""Header component for the Dash app."""

import dash_bootstrap_components as dbc
from dash import html


def create_header(pathname: str = '/') -> html.Header:
    """Create the accessible header component with skip link and semantic HTML.

    Args:
        pathname: Current page path to highlight the active navigation item
    """
    search_bar = dbc.InputGroup(
        [
            dbc.Input(
                type='search',
                placeholder='Search',
                id='header-search',
                name='search',
            ),
            dbc.InputGroupText(html.I(className='fa fa-magnifying-glass'), className='bg-grey border-0'),
        ],
        className='rounded-pill',
        style={'width': '30vw', 'overflow': 'hidden'},
    )

    brand = dbc.NavbarBrand(
        'LocABS',
        href='/',
        style={'font-weight': 'bold', 'font-size': '24px', 'color': 'white'},
    )

    nav_bar = html.Nav(
        dbc.Navbar(
            [
                brand,
                dbc.NavItem(
                    dbc.NavLink(
                        'Dashboard',
                        href='/dashboard',
                        active=pathname == '/dashboard',
                        className='nav-link-active' if pathname == '/dashboard' else 'nav-link-inactive',
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        'Scenario Builder',
                        href='/scenario-builder',
                        active=pathname == '/scenario-builder',
                        className='nav-link-active' if pathname == '/scenario-builder' else 'nav-link-inactive',
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        'Data Visualisation',
                        href='/data-viz',
                        active=pathname == '/data-viz',
                        className='nav-link-active' if pathname == '/data-viz' else 'nav-link-inactive',
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        'Decision Support',
                        href='/decision-support',
                        active=pathname == '/decision-support',
                        className='nav-link-active' if pathname == '/decision-support' else 'nav-link-inactive',
                    )
                ),
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem(
                            'Report',
                            href='/reports',
                            active=pathname == '/reports',
                            className='dropdown-item-active' if pathname == '/reports' else '',
                        ),
                        dbc.DropdownMenuItem(
                            'Developers',
                            href='/developers',
                            active=pathname == '/developers',
                            className='dropdown-item-active' if pathname == '/developers' else '',
                        ),
                        dbc.DropdownMenuItem(
                            'Help/FAQs',
                            href='/help',
                            active=pathname == '/help',
                            className='dropdown-item-active' if pathname == '/help' else '',
                        ),
                    ],
                    label='More',
                    nav=True,
                    className='nav-link-active'
                    if pathname in ['/reports', '/developers', '/help']
                    else 'nav-link-inactive',
                ),
                search_bar,
            ],
            color='black',
            className='navbar d-flex justify-content-evenly align-items-center font-weight-bold text-white',
            style={
                'padding': '20px 10px',
            },
        )
    )

    return html.Header(
        [
            dbc.Container(
                [nav_bar],
                className='app-header',
                style={
                    'padding': '0px',
                    'position': 'relative',
                    'top': '0',
                    'left': '0',
                    'right': '0',
                    'zIndex': '1000',
                    'margin': '0',
                    'backgroundColor': 'white',
                },
                fluid=True,
            ),
        ]
    )
