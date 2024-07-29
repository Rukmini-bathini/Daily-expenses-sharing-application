# create_db.py
from app import app, db
from models.user import User
from models.expense import Expense
from models.expense_split import ExpenseSplit

with app.app_context():
    db.create_all()

    if not User.query.first():
        user1 = User(email='test1@example.com', name='Test User 1', mobile_number='1234567890')
        user2 = User(email='test2@example.com', name='Test User 2', mobile_number='0987654321')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        expense1 = Expense(description='Dinner', amount=100, payer_id=user1.id, split_method='equal')
        db.session.add(expense1)
        db.session.commit()

        split1 = ExpenseSplit(expense_id=expense1.id, user_id=user1.id)
        split2 = ExpenseSplit(expense_id=expense1.id, user_id=user2.id)
        db.session.add(split1)
        db.session.add(split2)
        db.session.commit()

