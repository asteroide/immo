import base64
import dash
import dash.exceptions
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import logging
import yaml
import components.utils

__name__ = "Configuration"
logger = logging.getLogger("immo.configuration")


def define_callback(app):

    @app.callback(
        dash.dependencies.Output('coef_rent', 'value'),
        [Input('cache', 'children')]
    )
    def update_coef_rent(data):
        data = base64.b64decode(data)
        conf = yaml.load(data)
        return conf.get("configuration").get("coef_rent", 9)

    @app.callback(
        dash.dependencies.Output('coef_price', 'value'),
        [Input('cache', 'children')]
    )
    def update_coef_price(data):
        data = base64.b64decode(data)
        conf = yaml.load(data)
        return conf.get("configuration").get("coef_price", 2500)

    @app.callback(
        dash.dependencies.Output('coef_work', 'value'),
        [Input('cache', 'children')]
    )
    def update_coef_work(data):
        data = base64.b64decode(data)
        conf = yaml.load(data)
        return conf.get("configuration").get("coef_work", 10)

    @app.callback(
        dash.dependencies.Output('coef_taxes', 'value'),
        [Input('cache', 'children')]
    )
    def update_coef_taxes(data):
        data = base64.b64decode(data)
        conf = yaml.load(data)
        return conf.get("configuration").get("coef_taxes", 10)

    @app.callback(
        Output('cache', 'children'),
        [Input('upload', 'contents')])
    def upload_callback(content):
        if not content:
            return
        header, _, data = content.partition(';')
        if header != "data:application/x-yaml":
            logger.error("Not a YAML file ({})".format(header))
            return
        enc, _, data = data.partition(',')
        if enc != "base64":
            logger.error("Not a base64 encoded file ({})".format(enc))
            return
        # data = base64.b64decode(data)
        # conf = yaml.load(data)
        # logger.warning("data={}".format(conf))
        logger.warning("File content is {}".format(data))
        return data
        # dff = pd.read_csv(io.StringIO(content))
        # return dff.to_dict('records')


def get_component(**kwargs):
    app = kwargs.get("app")
    conf = kwargs.get("conf", {})

    upload = dcc.Upload(
        id='upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
        }
    )
    logger.warning("coef_rent {}".format(conf.get("configuration")))
    logger.warning("coef_rent {}".format(conf.get("configuration").get("coef_rent", 9)))
    coef_rent = components.utils.SingleInput(
        "Coefficient multiplicateur pour les loyers", "coef_rent", app=app)
    coef_rent.min = 0
    coef_rent.max = 20
    coef_rent.step = 1
    coef_rent.value = conf.get("configuration").get("coef_rent", 9)
    coef_rent.marks = {5*x: 5*x for x in range(4)}
    coef_price = components.utils.SingleInput(
        "Coefficient multiplicateur pour le prix des logements", "coef_price", app=app)
    coef_price.min = 0
    coef_price.max = 3000
    coef_price.step = 10
    coef_price.value = 2500
    coef_price.marks = {500*x: 500*x for x in range(6)}
    coef_work = components.utils.SingleInput(
        "Coefficient multiplicateur pour les travaux à effectuer "
        "chaque année dans le logement en pourcentage", "coef_work", app=app)
    coef_work.min = 0
    coef_work.max = 100
    coef_work.step = 1
    coef_work.value = 10
    coef_work.marks = {20*x: "{}%".format(20*x) for x in range(5)}
    coef_taxes = components.utils.SingleInput(
        "Coefficient multiplicateur pour les impôts sur les plus-values "
        "en pourcentage",
        "coef_taxes", app=app)
    coef_taxes.min = 0
    coef_taxes.max = 100
    coef_taxes.step = 1
    coef_taxes.value = 10
    coef_taxes.marks = {20*x: "{}%".format(20*x) for x in range(5)}
    # try:
    #     define_callback(app)
    # except dash.exceptions.CantHaveMultipleOutputs:
    #     pass
    return html.Div(
        children=[
            upload,
            html.Div(id='upload-information'),
            coef_rent.get(),
            coef_price.get(),
            coef_work.get(),
            coef_taxes.get()
        ]
    )
