import dash_html_components as html

__name__ = "Graphiques"


def get_component(**kwargs):
    return html.Div(
        children=[
            html.Label('Configuration'),
        ]
    )



