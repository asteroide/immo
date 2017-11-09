import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import logging

logger = logging.getLogger("immo.utils")


class SingleInput:
    style_label = {
        "display": "inline-block",
        "vertical-align": "top",
        "text-align": "right",
        "padding": 10,
        "width": 250
    }
    margin_style = {
        # 'paddingBottom': 5, 'paddingTop': 5,
        # # 'marginBottom': 5, 'marginTop': 15,
        # 'marginRight': 5, 'marginLeft': 5,
        'margin-left': 'auto',
        'margin-right': 'auto'
    }

    def __init__(self, title="NC", id=None, **kwargs):
        self.title = title
        self.app = kwargs.get("app")
        if not id:
            self.id = self.title.replace(" ", "_")
        else:
            self.id = id
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get(self):
        component = html.Div(children=[
            html.Label(self.title, style=self.style_label),
            # html.Div(
            #     children=[
            #         dcc.Slider(
            #             id="slider_"+self.id,
            #             min=getattr(self, "min", 0),
            #             max=getattr(self, "max", 1000),
            #             step=getattr(self, "step", 100),
            #             value=getattr(self, "value", 0),
            #             marks=getattr(self, "marks", {}),
            #         ),
            #     ],
            #     style={
            #         "vertical-align": "top",
            #         "display": "inline-block",
            #         "width": "25%",
            #         "margin": 20
            #     }
            # ),
            dcc.Input(value=getattr(self, "value", 100), type='number',
                      step=getattr(self, "step", 100), id=self.id,
                      style={"vertical-align": "top",
                             "display": "inline-block",
                             "width": 100,
                             "margin": 10}
                      )
        ],
            style=self.margin_style
        )

        # @self.app.callback(
        #     dash.dependencies.Output(self.id, 'value'),
        #     [Input("slider_"+self.id, 'value')]
        # )
        # def update(data):
        #     logger.warning("update={}".format(update))
        #     return data
        return component


class MultiInput:
    style_label = {
        "display": "inline-block",
        "vertical-align": "top",
        "text-align": "right",
        "padding": 10,
        "width": 250
    }
    margin_style = {
        # 'paddingBottom': 5, 'paddingTop': 5,
        # # 'marginBottom': 5, 'marginTop': 15,
        # 'marginRight': 5, 'marginLeft': 5,
        'margin-left': 'auto',
        'margin-right': 'auto'
    }

    def __init__(self, title="NC", id=None, **kwargs):
        self.title = title
        self.app = kwargs.get("app")
        if not id:
            self.id = self.title.replace(" ", "_")
        else:
            self.id = id
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get(self):
        component = html.Div(children=[
            html.Label(self.title, style=self.style_label),
            html.Div(
                children=[
                    dcc.Slider(
                        id="slider_"+self.id,
                        min=getattr(self, "min", 0),
                        max=getattr(self, "max", 1000),
                        step=getattr(self, "step", 100),
                        value=getattr(self, "value", 0),
                        marks=getattr(self, "marks", {}),
                    ),
                ],
                style={
                    "vertical-align": "top",
                    "display": "inline-block",
                    "width": "25%",
                    "margin": 20
                }
            ),
            dcc.Input(value=getattr(self, "value", 100), type='number',
                      step=getattr(self, "step", 100), id=self.id,
                      style={"vertical-align": "top",
                             "display": "inline-block",
                             "width": 100,
                             "margin": 10}
                      )
        ],
            style=self.margin_style
        )

        # @self.app.callback(
        #     dash.dependencies.Output(self.id, 'value'),
        #     [Input("slider_"+self.id, 'value')]
        # )
        # def update(data):
        #     logger.warning("update={}".format(update))
        #     return data
        return component


def emprunt2csv(emprunt):
    result = ""
    for line in emprunt:
        result += str(line['montant']) + "," + str(line['duree']/12) + "\n"
    return result


def csv2emprunt(data):
    result = []
    for line in data.splitlines():
        values = line.split(',')
        try:
            result.append(
                {"montant": int(values[0]), "duree": float(values[1]) * 12}
            )
        except ValueError:
            pass
    return result


