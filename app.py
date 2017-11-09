# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import logging
import datetime
import time

from core import utils

logger = logging.getLogger("immo")

app = dash.Dash()
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

data = {
    "loyer": 500,
    "prix": 100000,
    "apport": 50000,
    "surface": 60,
    "taxes": 1000,
    "impots": 0.5,
}
# Emprunts possibles
# TODO : à mettre dans un tableau

multiplicateur_loyer = 9
multiplicateur_achat = 2500
coef_travaux = 0.1
emprunt = [
    {"montant": 100, "duree": 33 * 12},
    {"montant": 150, "duree": 31 * 12},
    {"montant": 200, "duree": 29 * 12},
    {"montant": 250, "duree": 27 * 12},
    {"montant": 300, "duree": 25 * 12},
    {"montant": 350, "duree": 22.5 * 12},
    {"montant": 400, "duree": 20 * 12},
    {"montant": 450, "duree": 17.5 * 12},
    {"montant": 500, "duree": 15 * 12},
    {"montant": 550, "duree": 12.5 * 12},
    {"montant": 600, "duree": 10 * 12},
    {"montant": 650, "duree": 7.5 * 12},
    {"montant": 700, "duree": 5 * 12},
]
duree_max_emprunt = max([x["duree"] for x in emprunt])

style = {
    'background': '#CCCCCC',
    'output-background': '#AAAAAA',
    'text': '#000000',
    'margin': "5px",
}

style_label = {
    "display": "inline-block",
    "vertical-align": "top",
    "text-align": "right",
    "padding": 10,
    "width": 250
}
margin_style = {
    'paddingBottom': 5, 'paddingTop': 5,
    # 'marginBottom': 5, 'marginTop': 15,
    'marginRight': 5, 'marginLeft': 15,
}


def get_config():
    yield html.Div(
        children=[
            html.Div(
                children=[
                    html.Label('Loyer en €', style=style_label),
                    html.Div(
                        children=[
                            dcc.Slider(
                                id="loyer_slider",
                                min=0,
                                max=1000,
                                step=10,
                                value=500,
                                marks={x: "{}€".format(x) for x in range(0, 1000, 100)},
                            ),
                        ],
                        style={
                            "vertical-align": "top",
                            "display": "inline-block",
                            "width": "50%"
                        }
                    ),
                    dcc.Input(value='500', type='number', step=10, id="loyer",
                              style={"vertical-align": "top",
                                     "display": "inline-block",
                                     "width": 150}
                              ),
                ],
                style=margin_style
            ),
            html.Div(children=[
                    html.Label("Prix d'achat", style=style_label),
                    html.Div(
                        children=[
                            dcc.Slider(
                                id="prix_slider",
                                min=0,
                                max=300000,
                                step=1000,
                                value=100000,
                                marks={x: "{}€".format(x) for x in range(0, 300000, 50000)},
                            ),
                        ],
                        style={
                            "vertical-align": "top",
                            "display": "inline-block",
                            "width": "50%"
                        }
                    ),
                    dcc.Input(value='100000', type='number', step=1000, id="prix",
                              style={"vertical-align": "top",
                                     "display": "inline-block",
                                     "width": 150}
                              )
                ],
                style=margin_style
            ),
            html.Div(children=[
                    html.Label("Apport", style=style_label),
                    html.Div(
                        children=[
                            dcc.Slider(
                                id="apport_slider",
                                min=0,
                                max=50000,
                                step=1000,
                                value=10000,
                                marks={x: "{}€".format(x) for x in range(0, 50000, 10000)},
                            ),
                        ],
                        style={
                            "vertical-align": "top",
                            "display": "inline-block",
                            "width": "50%"
                        }
                    ),
                    dcc.Input(value='50000', type='number', step=1000, id="apport",
                              style={"vertical-align": "top",
                                     "display": "inline-block",
                                     "width": 150}
                              )
                ],
                style=margin_style
            ),
            html.Div(children=[
                    html.Label("Surface", style=style_label),
                    html.Div(
                        children=[
                            dcc.Slider(
                                id="surface_slider",
                                min=0,
                                max=100,
                                step=1,
                                value=50,
                                marks={x: "{}m²".format(x) for x in range(0, 100, 10)},
                            ),
                        ],
                        style={
                            "vertical-align": "top",
                            "display": "inline-block",
                            "width": "50%"
                        }
                    ),
                    dcc.Input(value='50', type='number', step=1, id="surface",
                              style={"vertical-align": "top",
                                     "display": "inline-block",
                                     "width": 150}
                              )
                ],
                style=margin_style
            ),
            html.Div(children=[
                    html.Label("Taxes annuelles", style=style_label),
                    dcc.Input(value='1000', type='number', step=100, id="taxes",
                              style={"vertical-align": "top",
                                     "display": "inline-block",
                                     "width": 150}
                              )
                ],
                style=margin_style
            ),
            html.Div(children=[
                    html.Label("Pourcentage impôts", style=style_label),
                    dcc.Input(value='0.5', type='number', step=0.1, id="impots",
                              style={"vertical-align": "top",
                                     "display": "inline-block",
                                     "width": 150}
                              )
                ],
                style=margin_style
            ),
            html.Div(children=[
                html.Label("Liste des emprunts", style=style_label),
                dcc.Textarea(
                    id="emprunts",
                    placeholder='Enter a value...',
                    value=utils.emprunt2csv(emprunt),
                    style={"height": 50, "vertical-align": "top",
                           "display": "inline-block",
                                     "width": 150}
                )
            ],
                style=margin_style
            )
        ],
        style={
            'backgroundColor': style['output-background'],
            # 'text-align': "center",
            'marginRight': "20%", 'marginLeft': "20%",
            'border-radius': 10
        }
    )


def get_global_result():
    yield html.Div(
        children=[
            html.Div(
                id='output-rentabilite',
                children=[],
                style={
                    'backgroundColor': style['output-background'],
                    'display': 'inline-block',
                }
            ),
            html.Br(),
            html.Div(
                id='output-loyer',
                children=[],
                style={
                    'backgroundColor': style['output-background'],
                    'display': 'inline-block',
                }
            ),
            html.Label('(Loyer moyen au €/m²', style={"marginLeft": 30, "color": "#555555"}),
            dcc.Input(value='9', type='number', step=0.1, id="loyer_moyen"),
            html.Label(')', style={"color": "#555555"}),
            html.Br(),
            html.Div(
                id='output-prix',
                children=[],
                style={
                    'backgroundColor': style['output-background'],
                    'display': 'inline-block',
                }
            ),
            html.Label('(Prix moyen au €/m²', style={"marginLeft": 30, "color": "#555555"}),
            dcc.Input(value='2500', type='number', step=10, id="prix_moyen"),
            html.Label(')', style={"color": "#555555"}),
        ],
        style={
            'backgroundColor': style['output-background'],
            'text-align': "center",
            'marginBottom': 20, 'marginTop': 20,
            'marginRight': "20%", 'marginLeft': "20%",
            'border-radius': 10
        }
    )


def get_graph():
    yield dcc.Graph(
        id='graph',
        figure={'layout': {
            'plot_bgcolor': style['background'],
            'paper_bgcolor': style['background'],
            'font': {
                'color': style['text']
            }
        }}
    )


app.layout = html.Div(
    style={
        'backgroundColor': style['background'],
        # 'color': style['text'],
        # 'padding': style['margin'],
        # 'columnCount': 2
        # 'paddingBottom': 10, 'paddingTop': 15,
        # 'paddingRight': 10, 'paddingLeft': 15,
        # 'marginBottom': 10, 'marginTop': 15,
        # 'marginRight': 10, 'marginLeft': 15,
    },
    children=[
        html.Div(
            html.H1(children='Calculateur de rentabilité'),
            style={
                'textAlign': 'center',
            },
        ),
        html.Div(
            children=list(get_config()),
            style={
                # 'paddingBottom': 5, 'paddingTop': 5,
                # 'marginBottom': 5, 'marginTop': 5,
                'marginRight': 10, 'marginLeft': 10,
                # 'columnCount': 2,
                # 'backgroundColor': style['output-background']
            },
        ),
        html.Div(
            id="global_result",
            children=list(get_global_result()),
        ),
        html.Div(
            children=list(get_graph())
        ),
])


def get_x():
    now = time.gmtime()
    for month in range(duree_max_emprunt):
        year = int(month/12)
        yield datetime.datetime(now.tm_year+year, month%12+1, 1)


@app.callback(
    dash.dependencies.Output('loyer', 'value'),
    [Input('loyer_slider', 'value')]
)
def update_loyer(loyer_slider):
    return loyer_slider


@app.callback(
    dash.dependencies.Output('prix', 'value'),
    [Input('prix_slider', 'value')]
)
def update_loyer(prix_slider):
    return prix_slider


@app.callback(
    dash.dependencies.Output('apport_slider', 'max'),
    [Input('prix', 'value')]
)
def update_apport_max(prix):
    return prix


@app.callback(
    dash.dependencies.Output('apport_slider', 'marks'),
    [Input('prix', 'value')]
)
def update_apport_marks(prix):
    increment = 10000
    if prix/5 < 100:
        increment = 50
    elif prix/5 < 2000:
        increment = 1000
    elif prix/5 < 20000:
        increment = 10000
    elif prix/5 < 50000:
        increment = 50000
    elif prix/5 < 200000:
        increment = 50000
    elif prix/5 < 2000000:
        increment = 5000000
    return {x: "{}€".format(x) for x in range(0, prix, increment)}


@app.callback(
    dash.dependencies.Output('apport_slider', 'value'),
    [Input('prix', 'value')]
)
def update_apport_marks(prix):
    return 0


@app.callback(
    dash.dependencies.Output('apport', 'value'),
    [Input('apport_slider', 'value')]
)
def update_loyer(apport_slider):
    return apport_slider


@app.callback(
    dash.dependencies.Output('surface', 'value'),
    [Input('surface_slider', 'value')]
)
def update_apport_max(surface):
    return surface


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [
        Input('loyer', 'value'),
        Input('taxes', 'value'),
        Input('impots', 'value'),
        Input('emprunts', 'value'),
    ])
def update_graph(loyer, taxes, impots, emprunts):
    datas = []
    legende = []
    loyer = int(loyer)
    taxes = int(taxes)
    impots = float(impots)
    for _emprunt in utils.csv2emprunt(emprunts):
        gain = [0, ]
        gain_somme = 0
        for mois in range(1, duree_max_emprunt):
            montant = _emprunt["montant"]
            if mois > int(_emprunt["duree"]):
                montant = 0
            gain_somme += loyer-montant
            if mois%12 == 0:
                gain_somme = gain_somme
                gain.append(gain[mois-1]+loyer*(1-coef_travaux)-montant-taxes-gain_somme*impots)
                gain_somme = 0
            else:
                gain.append(gain[mois-1]+loyer*(1-coef_travaux)-montant)

        data = go.Scatter(
            x=list(get_x()),
            y=gain,
            name="Emprunt à {}€".format(_emprunt["montant"]),
            #line=dict(
            #    color="rgb(255,0,0)",
            #    # shape='spline'
            #)
        )
        datas.append(data)
    return {
            "data": datas,
            "layout": go.Layout(
                title="Rentabilité",
                xaxis=dict(title='Temps en mois'),
                yaxis=dict(title='Montant en euros'),
            )
        }


@app.callback(Output('output-rentabilite', 'children'),
              [
                  Input('loyer', 'value'),
                  Input('prix', 'value'),
                  Input('apport', 'value'),
                  Input('taxes', 'value'),
              ])
def update_output_rentabilite(loyer, prix, apport, taxes):
    global data
    data["loyer"] = int(loyer)
    data["prix"] = int(prix)
    data["apport"] = int(apport)
    data["taxes"] = int(taxes)
    rentabilite = (data["loyer"] * 12 - data['taxes']) / (data['prix'] - data['apport'])
    return dcc.Markdown("""
Rentabilité brute : **{:.2%}**
    """.format(
        rentabilite,
    ))


@app.callback(Output('output-loyer', 'children'),
              [
                  Input('surface', 'value'),
                  Input('loyer_moyen', 'value'),
              ])
def update_output_loyer(surface, loyer_moyen):
    global data, multiplicateur_loyer
    if loyer_moyen:
        multiplicateur_loyer = float(loyer_moyen)
    data["surface"] = int(surface)
    return dcc.Markdown("""
Loyer possible : {:d} €
    """.format(
        int(int(surface) * multiplicateur_loyer),
    ))


@app.callback(Output('output-prix', 'children'),
              [
                  Input('surface', 'value'),
                  Input('prix_moyen', 'value'),
              ])
def update_output_prix(surface, prix_moyen):
    global data, multiplicateur_achat
    if prix_moyen:
        multiplicateur_achat = float(prix_moyen)
    data["surface"] = int(surface)
    return dcc.Markdown("""
Prix du marché : {} €
    """.format(
        int(surface) * multiplicateur_achat
    ))


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
