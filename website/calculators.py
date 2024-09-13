import plotly.express as px
import pandas as pd
import plotly.io as pio

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from jinja2 import Template, Environment, FileSystemLoader
from plotly.io import to_html

calculators = Blueprint('calculators', __name__)


@calculators.route('/compound-interest', methods=['GET', 'POST'])
def compoundInterestCalculator():
    return render_template("calc/compound_interest.html", user=current_user)


@calculators.route('/calculate-compound', methods=['GET', 'POST'])
def calculateCompound():
    if request.method == "POST":
        compounded, paid, plot_html = compoundInterest()
        return jsonify({'compounded': compounded, 'paid': paid, 'plot_html': plot_html})


def compoundInterest():
    deposit = float(request.json.get('deposit'))
    interest = float(request.json.get('interest')) / 100
    contribution = float(request.json.get('contribution'))
    compound_frequency = request.json.get('compound_frequency')
    investment_time = int(request.json.get('investment_time'))
    compounds_per_year = 1
    result = amount_paid = [deposit]
    amount_paid = [deposit]

    if compound_frequency == 'monthly':
        compounds_per_year = 12
    elif compound_frequency == 'quarterly':
        compounds_per_year = 4

    adj_interest = interest / compounds_per_year
    for year in range(investment_time):
        for period in range(compounds_per_year):
            deposit = deposit * (1 + adj_interest) + contribution
        result.append(round(deposit, 2))
        amount_paid.append(amount_paid[-1] + contribution * 12)

    df = pd.DataFrame(dict(
        Year=[x for x in range(investment_time + 1)],
        Value=result,
        Contribution=amount_paid,
    ))

    fig = px.line(df, x='Year', y=['Value', 'Contribution'], title="Compound Interest", markers=True,
                  labels={
                      'Year': 'Years after investment',
                      'value': 'Euros (€)',
                      'variable': 'Type'
                  }, )

    plot_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    return result[-1], amount_paid[-1], plot_html


@calculators.route('/financial-freedom', methods=['GET', 'POST'])
def financialFreedom():
    return render_template("calc/financial_freedom.html", user=current_user)
