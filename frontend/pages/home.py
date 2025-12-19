"""Homepage with documentation and navigation guide."""

import dash_bootstrap_components as dbc
from dash import html, register_page
from utilities.logging import configure_logger

configure_logger(level='DEBUG')

register_page(__name__, path='/', name='Home', title='LocABS · Home')


def create_workflow_step(number, title, description, button_text, button_href):
    """Create a workflow step with numbered circle and navigation button."""
    return dbc.Col(
        html.Div(
            [
                html.Div(str(number), className='workflow-circle'),
                html.H5(title, className='workflow-title'),
                html.P(description, className='workflow-description'),
                dbc.Button(
                    button_text,
                    href=button_href,
                    size='sm',
                    className='mt-2',
                    style={
                        'background-color': 'white',
                        'color': '#000',
                        'border': 'none',
                        'padding': '0.4rem 1rem',
                        'font-size': '12px',
                        'font-weight': '600',
                        'border-radius': '4px',
                    },
                ),
            ],
            className='workflow-step',
        ),
        lg=2,
        md=4,
        sm=6,
        xs=12,
        className='mb-3',
    )


def create_workflow_visual():
    """Create the main workflow visualization section with 5 steps."""
    return html.Div(
        html.Div(
            [
                html.H2('Getting Started', className='section-title'),
                html.P('Follow these steps to begin using the application', className='section-subtitle'),
                dbc.Row(
                    [
                        create_workflow_step(
                            1,
                            'Start with the Dashboard',
                            'Get an overview of your scenarios, simulations, and key metrics.',
                            'Go to Dashboard',
                            '/dashboard',
                        ),
                        create_workflow_step(
                            2,
                            'Explore Data Visualization',
                            'Create interactive charts and analyze your simulation data.',
                            'View Data',
                            '/data-viz',
                        ),
                        create_workflow_step(
                            3,
                            'Use Decision Support',
                            'Interact with Bayesian networks and evaluate intervention strategies.',
                            'Explore Tools',
                            '/decision-support',
                        ),
                        create_workflow_step(
                            4,
                            'Generate Info Reports',
                            'Document your findings and share insights with stakeholders.',
                            'Create Report',
                            '/reports',
                        ),
                        create_workflow_step(
                            5,
                            'Check Help/FAQs',
                            'Access detailed guidance, terminology, and troubleshooting assistance. Get access to workflow demo video.',
                            'Visit Help',
                            '/help',
                        ),
                    ],
                    className='workflow-steps-row',
                ),
            ],
            className='workflow-section',
        ),
    )


def create_cta_section():
    """Create a call-to-action section."""
    return html.Div(
        html.Div(
            [
                html.H2('Ready to Get Started?', className='cta-title'),
                html.P(
                    'Launch the dashboard and start configuring your first simulation. No installation, no setup—just powerful simulation management.',
                    className='cta-subtitle',
                ),
                dbc.Button(
                    ['Launch Dashboard Now ', html.I(className='fas fa-arrow-right ms-2')],
                    href='/dashboard',
                    className='cta-button',
                ),
            ],
            className='cta-content',
        ),
        className='cta-section',
    )


layout = html.Div(
    [
        html.Main(
            html.Div(
                [
                    # Hero section
                    html.Div(
                        [
                            html.H1('WELCOME TO LOCABS', className='hero-title'),
                            html.P(
                                'The Location-Based Agent Simulation System is a comprehensive platform designed to help researchers, analysts, and policymakers visualize and interact with simulated spatial data for informed decision-making.',
                                className='hero-subtitle',
                            ),
                        ],
                        className='hero-section',
                    ),
                    # Workflow visual section
                    create_workflow_visual(),
                    # Use Cases & Applications section
                    html.Div(
                        [
                            html.H2('USE CASES & APPLICATIONS', className='section-title'),
                            # html.P('Real-world scenarios where LocABS excels', className='section-subtitle'),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.I(className='fas fa-virus fa-3x platform-icon'),
                                                    html.H5(
                                                        'Disease Outbreak Modeling', className='platform-card-title'
                                                    ),
                                                    html.P(
                                                        'Simulate infectious disease spread patterns, test intervention strategies, and predict outbreak trajectories in various population densities.',
                                                        className='platform-card-text',
                                                    ),

                                                ]
                                            ),
                                            className='platform-card',
                                        ),
                                        md=6,
                                        lg=3,
                                        className='mb-3',
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.I(className='fas fa-running fa-3x platform-icon'),
                                                    html.H5(
                                                        'Emergency Evacuation Planning', className='platform-card-title'
                                                    ),
                                                    html.P(
                                                        'Model crowd movement during emergencies, optimize exit routes, and evaluate facility layouts for safety compliance.',
                                                        className='platform-card-text',
                                                    ),

                                                ]
                                            ),
                                            className='platform-card',
                                        ),
                                        md=6,
                                        lg=3,
                                        className='mb-3',
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.I(className='fas fa-notes-medical fa-3x platform-icon'),
                                                    html.H5(
                                                        'Public Health Policy Testing', className='platform-card-title'
                                                    ),
                                                    html.P(
                                                        'Evaluate the impact of health interventions, vaccination campaigns, and social distancing measures before implementation.',
                                                        className='platform-card-text',
                                                    ),
                                                ]
                                            ),
                                            className='platform-card',
                                        ),
                                        md=6,
                                        lg=3,
                                        className='mb-3',
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.I(className='fas fa-building fa-3x platform-icon'),
                                                    html.H5(
                                                        'Facility Layout Optimization', className='platform-card-title'
                                                    ),
                                                    html.P(
                                                        'Design optimal spatial configurations for offices, hospitals, and public spaces to maximize efficiency and safety.',
                                                        className='platform-card-text',
                                                    ),
                                                ]
                                            ),
                                            className='platform-card',
                                        ),
                                        md=6,
                                        lg=3,
                                        className='mb-3',
                                    ),
                                ]
                            ),
                        ],
                        className='platform-overview-section',
                    ),
                    # Call to action
                    create_cta_section(),
                    # Help section
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.I(className='fas fa-question-circle fa-2x platform-icon'),
                                                html.H5('Need Help?', className='platform-card-title'),
                                                html.P(
                                                    'Access comprehensive guides, tutorials, and troubleshooting resources.',
                                                    className='platform-card-text',
                                                ),
                                                dbc.Button(
                                                    'Visit Help Center',
                                                    href='/help',
                                                    className='platform-card-button',
                                                ),
                                            ]
                                        ),
                                        className='platform-card',
                                    ),
                                    md=4,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.I(className='fas fa-book fa-2x platform-icon'),
                                                html.H5('Documentation', className='platform-card-title'),
                                                html.P(
                                                    'Detailed technical documentation and API references for developers.',
                                                    className='platform-card-text',
                                                ),
                                                dbc.Button(
                                                    'Read Docs',
                                                    href='/developers',
                                                    className='platform-card-button',
                                                ),
                                            ]
                                        ),
                                        className='platform-card',
                                    ),
                                    md=4,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.I(className='fas fa-lightbulb fa-2x platform-icon'),
                                                html.H5('Decision Support', className='platform-card-title'),
                                                html.P(
                                                    'Tools for scenario comparison and evidence-based policy analysis.',
                                                    className='platform-card-text',
                                                ),
                                                dbc.Button(
                                                    'Explore Tools',
                                                    href='/decision-support',
                                                    className='platform-card-button',
                                                ),
                                            ]
                                        ),
                                        className='platform-card',
                                    ),
                                    md=4,
                                ),
                            ],
                            className='g-3',
                        ),
                        className='mb-4',
                    ),
                ],
                className='container-fluid px-4 py-3',
            ),
            id='main',
        ),
    ]
)
