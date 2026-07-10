"""FAQ Components for Dash Applications."""

import dash_bootstrap_components as dbc
from dash import html


class FAQSection(html.Div):
    """FAQ Section component."""

    def __init__(self, title: str, faqs: dict[str, str]) -> None:
        """Create new FAQ section from title and content."""
        section_id = title.lower().replace(' ', '-')

        faq_entries = []
        for idx, (question, answer) in enumerate(faqs.items()):
            faq_entries.append(
                dbc.AccordionItem(
                    html.P(answer, className='help-faq-answer'),
                    title=question,
                    item_id=f'{section_id}-{idx}',
                )
            )

        accordion = dbc.Accordion(
            faq_entries,
            id=f'accordion-{section_id}',
            start_collapsed=True,
            always_open=True,
            className='help-accordion',
        )
        super().__init__(
            [
                html.Div(f'FAQ: {title.upper()}', className='help-section-header'),
                html.Div(accordion, className='help-section-content'),
            ],
            className='help-faq-section',
        )
