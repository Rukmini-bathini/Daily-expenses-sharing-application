# models/expense_split.py
from models import db

class ExpenseSplit(db.Model):
    __tablename__ = 'expense_splits'

    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Numeric(10, 2))
    percentage = db.Column(db.Numeric(5, 2))

    expense = db.relationship('Expense')
    user = db.relationship('User')

    def to_dict(self):
        return {
            'id': self.id,
            'expense_id': self.expense_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'percentage': self.percentage
        }
