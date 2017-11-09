import dash
import dash_core_components as dcc
import dash.exceptions
from dash.dependencies import Input, Output, State
import dash_html_components as html
import logging
import components.utils

__name__ = "Données perso"
logger = logging.getLogger("immo.personal_data")

loaners = []


def define_callback(app):
    @app.callback(
        dash.dependencies.Output('debt_ratio', 'children'),
        [
            Input('salary', 'value'),
            Input('alimony', 'value'),
            Input('other_salary', 'value'),
            Input('credits', 'value'),
            Input('other_charge', 'value'),
        ]
    )
    def update_salary(salary, alimony, other_salary, credit, other_charge):
        logger.warning("{} {} {} {} {}".format(salary, alimony, other_salary, credit, other_charge))
        result = 1 - (
                         int(salary) +
                         int(alimony) +
                         int(other_salary) -
                         int(credit) -
                         int(other_charge)
                     ) / (int(salary) + int(alimony) + int(other_salary))
        logger.warning("result={}".format(result))
        return html.Div(
            children=[
                html.P("Taux d'endettement actuel : {:.2%}".format(result)),
                html.Div(children=[
                    dcc.Slider(
                        id="slider_debt_ratio",
                        min=0,
                        max=100,
                        value=100*result,
                        marks={33: "33%", 66: "66%"}
                    )],
                    style={
                        # "vertical-align": "top",
                        # "display": "inline-block",
                        "width": "25%",
                        # "margin": 20
                    }
                )
        ])


def get_component(**kwargs):
    app = kwargs.get("app")
    if not loaners:
        salary = components.utils.SingleInput(
            "Salaires (emprunteur & co-emprunteur) par mois", "salary", app=app)
        salary.value = 2000
        loaners.append(salary)

    alimony = components.utils.SingleInput(
        "Pension alimentaire par mois", "alimony", app=app)
    alimony.value = 0

    other_salary = components.utils.SingleInput(
        "Autre revenu par mois", "other_salary", app=app)
    other_salary.value = 0

    credits = components.utils.SingleInput(
        "Total des crédits par mois", "credits", app=app)
    credits.value = 0

    other_charge = components.utils.SingleInput(
        "Autre charge (par ex. loyer) par mois", "other_charge", app=app)
    other_charge.value = 0

    debt_ration = html.Div(id="debt_ratio")

    return html.Div(
        children=[
            html.Div(
                children=[x.get() for x in loaners]
            ),
            alimony.get(),
            other_salary.get(),
            credits.get(),
            other_charge.get(),
            debt_ration
        ]
    )
