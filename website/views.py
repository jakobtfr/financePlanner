import json

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

from . import db
from .models import Income


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':

        income = request.form.get('income')
        income_type = request.form.get('type')

        if not income or float(income) <= 0:
            flash("Income must be a positive number.", category='error')

        else:
            new_income = Income(amount=float(income), user_id=current_user.id, type=income_type)
            current_user.total_income += float(income)
            db.session.add(new_income)
            flash("Income added.", category='success')

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
            current_user.total_income -= float(income.amount)
            db.session.commit()

    return jsonify({})
