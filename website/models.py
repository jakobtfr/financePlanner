from . import db
from flask_login import UserMixin


class Money(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money_id = db.Column(db.Integer, db.ForeignKey('money.id'), nullable=False)
    type = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    money = db.relationship('Money', backref='incomes', lazy=True)

    @property
    def amount(self):
        return self.money.value if self.money else 0.0


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money_id = db.Column(db.Integer, db.ForeignKey('money.id'), nullable=False)
    type = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    money = db.relationship('Money', backref='expenses', lazy=True)

    @property
    def amount(self):
        return self.money.value if self.money else 0.0


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    incomes = db.relationship('Income', backref='user', lazy=True)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    @property
    def net(self):
        total_income = sum(income.money.value for income in self.incomes if income.money)
        total_expenses = sum(expense.money.value for expense in self.expenses if expense.money)
        return total_income - total_expenses

    @property
    def total_income(self):
        return sum(income.money.value for income in self.incomes if income.money)

    @property
    def total_expense(self):
        return sum(expense.money.value for expense in self.expenses if expense.money)

