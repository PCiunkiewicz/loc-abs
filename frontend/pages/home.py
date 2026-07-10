"""Homepage with documentation and navigation guide."""

import dash_bootstrap_components as dbc
from dash import html, register_page

register_page(__name__, path='/', name='Home', title='Loc-ABS - Home')


def workflow_step(number: int, title: str, description: str, button_text: str, button_href: str) -> dbc.Col:
    """Create a workflow step with numbered circle and navigation button."""
    return dbc.Col(
        html.Div(
            [
                html.Div(str(number), className='workflow-circle'),
                html.H5(title, className='workflow-title'),
                dbc.Button(
                    button_text,
                    href=button_href,
                    className='btn-secondary',
                    style={'border': 'none', 'borderRadius': '0.25rem', 'width': '12rem'},
                ),
                html.P(description, className='workflow-description'),
            ],
            className='workflow-step',
        ),
        lg=2,
        md=4,
        sm=6,
        xs=12,
        className='mb-3',
    )


def workflow_visual() -> html.Div:
    """Create the main workflow visualization section with 5 steps."""
    return html.Div(
        html.Div(
            [
                html.H2('Getting Started', className='section-title'),
                html.P('Follow these steps to begin using the application', className='section-subtitle'),
                dbc.Row(
                    [
                        workflow_step(
                            1,
                            'Build Your Scenario',
                            'Configure scenarios and population profiles for your simulations.',
                            'Build Scenario',
                            '/scenario-builder',
                        ),
                        workflow_step(
                            2,
                            'Data Visualization',
                            'Create interactive charts and analyze your simulation data.',
                            'View Data',
                            '/data-viz',
                        ),
                        workflow_step(
                            3,
                            'Decision Support',
                            'Interact with Bayesian networks and evaluate intervention strategies.',
                            'Explore Tools',
                            '/decision-support',
                        ),
                        workflow_step(
                            4,
                            'Generate Reports',
                            'Document your findings and share insights with stakeholders.',
                            'Create Report',
                            '/reports',
                        ),
                    ],
                    className='workflow-steps-row',
                ),
            ],
            className='workflow-section',
        ),
    )


layout = html.Div(
    [
        html.Main(
            html.Div(
                [
                    # Hero section
                    html.Div(
                        [
                            html.H1('Welcome to Loc-ABS', className='hero-title'),
                            html.P(
                                'The Localized Agent-Based Simulation framework is a comprehensive platform designed to help researchers, analysts, and policymakers visualize and interact with simulated spatial data for informed decision-making.',
                                className='hero-subtitle',
                            ),
                        ],
                        className='hero-section',
                    ),
                    # Workflow visual section
                    workflow_visual(),
                    # Use Cases & Applications section
                    html.Div(
                        [
                            html.H2('Use Cases and Applications', className='section-title'),
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
                    # Help section
                    html.H2('Resources', className='section-title'),
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
                                                    className='platform-card-button btn-secondary',
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
                                                    className='platform-card-button btn-secondary',
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
                                                    className='platform-card-button btn-secondary',
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
