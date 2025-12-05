"""Header component for the Dash app."""

import dash_bootstrap_components as dbc
from dash import html


def create_header() -> html.Div:
    """Create the header component for the Dash app."""
    search_bar = dbc.InputGroup(
        [
            dbc.Input(type='search', placeholder='Search here'),
            dbc.InputGroupText(html.I(className='fa fa-magnifying-glass'), className='bg-grey border-0'),
        ],
        className='rounded-pill',
        style={'width': '30vw', 'overflow': 'hidden'},
    )

    brand = dbc.NavbarBrand('LocABS', href='/', style={'font-weight': 'bold', 'font-size': '24px', 'color': 'white'})

    nav_bar = dbc.Navbar(
        [
            brand,
            dbc.NavItem(dbc.NavLink('Dashboard', href='/', active=True)),
            dbc.NavItem(dbc.NavLink('Scenario Builder', href='/scenario-builder')),
            dbc.NavItem(dbc.NavLink('Data Visualisation', href='/data-viz')),
            dbc.NavItem(dbc.NavLink('Decision Support', href='/decision-support')),
            dbc.NavItem(dbc.NavLink('Report', href='/reports')),
            dbc.DropdownMenu(
                [
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
            # "margin": "30px 0",
        },
    )

    return dbc.Container(
        [
            # dbc.Container([
            #     brand,
            #     search_bar,
            # ],
            # className="header-container d-flex justify-content-evenly align-items-center",
            # fluid=True,),
            nav_bar
        ],
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
    )
