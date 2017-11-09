import dash
import dash.exceptions
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import logging

from components import personal_data
from components import purchase_information
from components import loaning_information
from components import global_results
from components import graphes
from components import configuration
# import components.utils

logger = logging.getLogger("immo")

CONF = {
    "configuration": {},
    "personal": {},
    "loaning": {},
    "purchase": {},
}

TABS = [
    configuration,
    personal_data,
    purchase_information,
    loaning_information,
    global_results,
    graphes
]

app = dash.Dash()
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children='Calculateur de rentabilité'),
            ]
        ),
        dcc.Tabs(
            tabs=[
                {'label': TABS[index].__name__, 'value': index}
                for index in range(len(TABS))
            ],
            value=1,
            id='tabs',
            vertical=False
        ),
        html.Div(id='tab-output'),
        html.Div(id='cache', style={'display': 'none'})
    ], style={
        'width': '80%',
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto'
    },
)


# @app.callback(Output('information', 'children'),
#               [Input('save_button', 'n_clicks')])
# def save(value):
#     logger.warning("Clicking on save {}".format(value))
#     return html.P("Clicking on save {}".format(value))


@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def callback(value):
    logger.warning("Calling callback with {}".format(CONF))
    component = TABS[value].get_component(value=value, app=app, conf=CONF)
    return component


# @app.callback(
#     Output('information', 'children'),
#     [Input('upload', 'contents')])
# def upload_callback(content):
#     if not content:
#         logger.warning("no content {}".format(content))
#     logger.warning("File content is {}".format(content))


for comp in TABS:
    try:
        comp.define_callback(app)
    except dash.exceptions.CantHaveMultipleOutputs:
        pass
    except AttributeError:
        logger.error("Callbacks are not define for {}".format(comp.__name__))


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
