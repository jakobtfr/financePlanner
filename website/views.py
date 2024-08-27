import json

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
