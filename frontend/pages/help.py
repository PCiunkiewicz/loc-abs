"""Help Page for Loc-ABS Application."""

from dash import html, register_page

from components.faq import FAQSection

register_page(__name__, path='/help', name='Help', title='Loc-ABS - Help')

# FAQ Data Structure
FAQ_DATA = {
    'Getting Started': {
        'How do I create my first simulation?': 'To create your first simulation, navigate to the Run Builder page. Start by selecting or creating a scenario in Step 1, then configure your population in Step 2. Finally, review and launch your simulation in Step 3.',
        'What are the system requirements?': 'Loc-ABS runs in a web browser and requires Docker for deployment. Recommended browsers include Chrome, Firefox, or Edge. For optimal performance, use a system with at least 8GB RAM.',
        'How do I access my simulation results?': 'Navigate to the Dashboard page to view all completed simulations. Click on any simulation to view detailed results, or use the Data Visualization page for advanced analytics.',
    },
    'Scenario Configuration': {
        'What is a scenario?': 'A scenario represents a unique test condition that includes outbreak settings, protective measures, and simulation parameters. Each scenario can be reused across multiple simulation runs.',
        'How do I configure prevention measures?': 'In the Scenario Builder, navigate to the Protective Measures tab. Here you can configure masks, vaccines, social distancing policies, and other prevention strategies.',
        'Can I clone existing scenarios?': 'Yes! When viewing a scenario in the dropdown, click the "Clone" button to create a copy that you can modify without affecting the original.',
    },
    'Population Configuration': {
        'What are population profiles?': 'Population profiles define how individuals behave in the simulation, including movement patterns, social interactions, and compliance with protective measures.',
        'How many populations can I configure?': 'You can configure unlimited distinct population profiles, each representing a unique behavior pattern within your facility.',
        'What is the difference between population and profiles?': 'Population refers to the total number of individuals in the simulation, while profiles define the behavior categories. Multiple individuals can share the same profile.',
    },
    'Results & Analysis': {
        'How do I interpret simulation results?': 'The Dashboard provides key metrics including infection rates, duration, and status. Use the Data Visualization page for detailed charts and graphs showing transmission patterns over time.',
        'Can I export my results?': 'Yes! Navigate to the Data Visualization page and use the export functionality to download your simulation results in various formats.',
        'How long are results stored?': 'Simulation results are stored permanently in the database unless manually deleted. You can access historical runs at any time through the Dashboard.',
    },
}


layout = html.Div(
    [
        # Top Action Buttons
        html.Div(
            [
                html.Button(
                    [html.I(className='fa fa-rocket me-2'), 'GETTING STARTED'],
                    id='help-getting-started-btn',
                    className='btn help-action-btn',
                ),
                html.Button(
                    [html.I(className='fa fa-wrench me-2'), 'SCENARIO BUILDER'],
                    id='help-scenario-builder-btn',
                    className='btn help-action-btn',
                ),
                html.Button(
                    [html.I(className='fa fa-book me-2'), 'GLOSSARY TERMS'],
                    id='help-glossary-btn',
                    className='btn help-action-btn',
                ),
                html.Button(
                    [html.I(className='fa fa-headset me-2'), 'CONTACT SUPPORT'],
                    id='help-contact-btn',
                    className='btn help-action-btn',
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
                                    'Learn the basics of Loc-ABS in this comprehensive walkthrough. '
                                    'This 10-minute tutorial covers scenario creation, population configuration, and running your first simulation.',
                                    className='help-video-description',
                                ),
                                html.Button(
                                    [html.I(className='fa fa-play me-2'), 'Watch Tutorial'],
                                    className='btn-secondary help-video-btn',
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
                                    className='btn-secondary help-video-btn',
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
                                    className='btn-secondary help-video-btn',
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
                html.Div(
                    [
                        FAQSection('Getting Started', FAQ_DATA['Getting Started']),
                        FAQSection('Scenario Configuration', FAQ_DATA['Scenario Configuration']),
                    ],
                    className='help-faq-row',
                ),
                html.Div(
                    [
                        FAQSection('Population Configuration', FAQ_DATA['Population Configuration']),
                        FAQSection('Results & Analysis', FAQ_DATA['Results & Analysis']),
                    ],
                    className='help-faq-row',
                ),
            ],
            className='help-faq-container',
        ),
    ],
    className='help-page-container',
)
