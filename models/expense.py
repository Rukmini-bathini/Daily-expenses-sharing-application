# models/expense.py
from models import db

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    amount = db.Column(db.Float)
    payer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    split_method = db.Column(db.String(50))

    # Adding relationships when necessary
    payer = db.relationship('User', backref='expenses')

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'payer_id': self.payer_id,
            'split_method': self.split_method,
        }
