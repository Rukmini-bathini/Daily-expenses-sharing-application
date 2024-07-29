from flask import Flask, request, jsonify, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from models.user import User
from models.expense import Expense
from models.expense_split import ExpenseSplit
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://expense_user:password@localhost/expenses_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.form
    user = User(
        email=data['email'],
        name=data['name'],
        mobile_number=data['mobile_number']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.form
    expense = Expense(description=data['description'], amount=data['amount'], payer_id=data['payer_id'], split_method=data['split_method'])
    db.session.add(expense)
    db.session.commit()

    splits = request.form.get('splits', '[]')  # Get splits as JSON string and parse
    splits = eval(splits)  
    for split in splits:
        if expense.split_method == 'equal':
            split_amount = expense.amount / len(splits)
            expense_split = ExpenseSplit(expense_id=expense.id, user_id=split['user_id'], amount=split_amount)
        elif expense.split_method == 'exact':
            expense_split = ExpenseSplit(expense_id=expense.id, user_id=split['user_id'], amount=split['amount'])
        elif expense.split_method == 'percentage':
            split_amount = expense.amount * (split['percentage'] / 100)
            expense_split = ExpenseSplit(expense_id=expense.id, user_id=split['user_id'], amount=split_amount)
        db.session.add(expense_split)

    db.session.commit()
    return render_template('index.html', message="Expense added successfully!")

@app.route('/expenses/balance-sheet', methods=['GET'])
def get_balance_sheet():
    try:
        expenses = Expense.query.all()
        balance_sheet = {}

        # Initialize users in the balance sheet
        users = User.query.all()
        for user in users:
            balance_sheet[user.id] = {'paid': 0.0, 'owed': 0.0, 'total_expense': 0.0, 'name': user.name}

        for expense in expenses:
            amount = float(expense.amount)
            payer_id = expense.payer_id
            splits = ExpenseSplit.query.filter_by(expense_id=expense.id).all()

            if expense.split_method == 'equal':
                split_amount = amount / len(splits)
            elif expense.split_method == 'exact':
                split_amount = None
            elif expense.split_method == 'percentage':
                split_amount = None

            # Add to payer's total paid
            balance_sheet[payer_id]['paid'] += amount

            for split in splits:
                user_id = split.user_id
                if expense.split_method == 'equal':
                    split_amount = amount / len(splits)
                elif expense.split_method == 'exact':
                    split_amount = float(split.amount) if split.amount else 0.0
                elif expense.split_method == 'percentage':
                    split_amount = amount * (float(split.percentage) / 100) if split.percentage else 0.0

                # Add to each user's owed amount
                balance_sheet[user_id]['owed'] += split_amount

        # Calculate total expenses and update balance sheet
        for user_id, info in balance_sheet.items():
            info['total_expense'] = info['owed']
            if info['paid'] == 0:
                info['total_expense'] = info['owed']

        df = pd.DataFrame([
            {'user': user_id, 'user_name': info['name'], 'total_paid': info['paid'], 'total_expense': info['total_expense']}
            for user_id, info in balance_sheet.items()
        ])
        
        overall_expense = df['total_expense'].sum()

        # Add overall expense row
        df = df.append({'user': 'Overall Expenses', 'user_name': 'Overall', 'total_paid': df['total_paid'].sum(), 'total_expense': overall_expense}, ignore_index=True)

        # Generate CSV in-memory
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        return send_file(csv_buffer, mimetype='text/csv', download_name='balance_sheet.csv', as_attachment=True)
    except Exception as e:
        print(f"Error generating balance sheet: {e}")
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
