"""Header component for the Dash app."""

import dash_bootstrap_components as dbc
from dash import html


def create_header() -> html.Header:
    """Create the accessible header component with skip link and semantic HTML."""
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
                dbc.NavItem(dbc.NavLink('Dashboard', href='/dashboard', active=True)),
                dbc.NavItem(dbc.NavLink('Scenario Builder', href='/scenario-builder')),
                dbc.NavItem(dbc.NavLink('Data Visualisation', href='/data-viz')),
                dbc.NavItem(dbc.NavLink('Decision Support', href='/decision-support')),

                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem('Report', href='/reports'),
                        dbc.DropdownMenuItem('Developers', href='/developers'),
                        dbc.DropdownMenuItem('Help/FAQs', href='/help'),
                    ],
                    label='More',
                    nav=True,
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
