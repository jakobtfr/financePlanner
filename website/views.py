import json
import plotly.graph_objs as go
import plotly.io as pio

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

from . import db
from .models import Income, Expense, Money

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':

        income = request.form.get('income')
        income_type = request.form.get('type').title()

        expense = request.form.get('expense')
        expense_type = request.form.get('expense_type').title()

        existing_income = Income.query.filter_by(type=income_type, user_id=current_user.id).first()
        existing_expense = Expense.query.filter_by(type=expense_type, user_id=current_user.id).first()

        if not income and not expense:
            flash("Add an income or expense", category='error')
        else:
            if income:
                money = Money(value=income)
                db.session.add(money)
                db.session.commit()

                if existing_income:
                    existing_income.money.value += float(income)
                else:
                    new_income = Income(money_id=money.id, user_id=current_user.id, type=income_type)
                    db.session.add(new_income)

            if expense:
                money = Money(value=expense)
                db.session.add(money)
                db.session.commit()

                if existing_expense:
                    existing_expense.money.value += float(expense)
                else:
                    new_expense = Expense(money_id=money.id, user_id=current_user.id, type=expense_type)
                    db.session.add(new_expense)

            flash("Updated Income / Expense.", category='success')

        db.session.commit()

    return render_template("home.html", user=current_user)


@views.route('/delete-income', methods=['POST'])
def delete_income():
    data = json.loads(request.data)
    income_id = data['incomeId']
    income = Income.query.get(income_id)
    if income:
        if income.user_id == current_user.id:
            db.session.delete(income)
            db.session.delete(income.money)
            db.session.commit()

    return jsonify({})


@views.route('/delete-expense', methods=['POST'])
def delete_expense():
    data = json.loads(request.data)
    expense_id = data['expenseId']
    expense = Expense.query.get(expense_id)
    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense)
            db.session.delete(expense.money)
            db.session.commit()

    return jsonify({})


@views.route('/generate-sankey', methods=['GET'])
def generate_sankey():
    incomes = db.session.query(Income).filter_by(user_id=current_user.id).all()
    expenses = db.session.query(Expense).filter_by(user_id=current_user.id).all()

    if not incomes and not expenses:
        flash("Add an income or expense", category='error')
    else:
        income_amount = [income.amount for income in incomes]
        expense_amount = [expense.amount for expense in expenses]

        income_types = [income.type for income in incomes]
        expense_types = [expense.type for expense in expenses]

        budget = sum(income_amount)
        total_expenses = sum(expense_amount)

        total_amounts = income_amount + [budget] + expense_amount
        labels = income_types + ['Budget'] + expense_types

        source = []
        target = []
        value = []

        budget_index = len(income_types)

        for i in range(budget_index):
            source.append(i)
            target.append(budget_index)
            value.append(total_amounts[i])

        for i in range(budget_index + 1, len(labels)):
            source.append(budget_index)
            target.append(i)
            value.append(total_amounts[i])

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=10,
                line=dict(color="black", width=1),
                label=labels,
                color="blue",
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            ))])
        if budget < total_expenses:
            title = dict(text="Expenses are higher than budget!",
                         font=dict(color="red"))
            fig.update_layout(
                title=dict(text="Overview", subtitle=title),
            )
        else:
            fig.update_layout(
                title=dict(text="Overview")
            )

        fig.show()
        plot_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

        return jsonify({'plot_html' : plot_html})
