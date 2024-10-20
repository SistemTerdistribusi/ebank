from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from decimal import Decimal
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all domains to access your API

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ebanking:hexagon123@panel.honjo.web.id:3306/ebanking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'wibunyel'

# Initialize the database
db = SQLAlchemy(app)

@app.context_processor
def inject_current_datetime():
    current_datetime = datetime.now(pytz.timezone('Asia/Jakarta'))
    current_date = current_datetime.strftime('%d/%m/%Y')
    current_time = current_datetime.strftime('%H:%M:%S')
    return dict(current_date=current_date, current_time=current_time)


# Define the Customer model
class Customer(db.Model):
    __tablename__ = 'm_customer'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    customer_name = db.Column(db.String(30), nullable=False)
    customer_username = db.Column(db.String(50), nullable=False, unique=True)
    customer_pin = db.Column(db.String(200), nullable=False)  # Store hashed pin
    customer_phone = db.Column(db.String(20), nullable=True)
    customer_email = db.Column(db.String(50), nullable=True)
    cif_number = db.Column(db.String(30), nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime, nullable=True)
    created = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    updated = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)

# Define the PortfolioAccount model
class PortfolioAccount(db.Model):
    __tablename__ = 'm_portfolio_account'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    m_customer_id = db.Column(db.BigInteger, nullable=True)
    account_number = db.Column(db.String(20), nullable=True)
    account_status = db.Column(db.String(1), nullable=True)
    account_name = db.Column(db.String(50), nullable=True)
    account_type = db.Column(db.String(10), nullable=True)
    product_code = db.Column(db.String(10), nullable=True)
    product_name = db.Column(db.String(50), nullable=True)
    currency_code = db.Column(db.String(3), nullable=True)
    branch_code = db.Column(db.String(10), nullable=True)
    plafond = db.Column(db.Numeric(30, 5), nullable=True)
    clear_balance = db.Column(db.Numeric(30, 5), nullable=True)
    available_balance = db.Column(db.Numeric(30, 5), nullable=True)
    confidential = db.Column(db.String(1), nullable=True)
    created = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    created_by = db.Column(db.BigInteger, nullable=False, default=1)
    updated = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    updated_by = db.Column(db.BigInteger, nullable=False, default=1)

# Define the Transaction model
class Transaction(db.Model):
    __tablename__ = 't_transaction'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    m_customer_id = db.Column(db.BigInteger, nullable=False)
    transaction_type = db.Column(db.String(2), nullable=False, default='')
    transaction_amount = db.Column(db.Numeric(30, 5), nullable=True)
    transmission_date = db.Column(db.DateTime, nullable=True)
    transaction_date = db.Column(db.DateTime, nullable=True)
    value_date = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(250), nullable=True)
    status = db.Column(db.String(10), nullable=False, default='SUCCESS')
    created = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    updated = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)






# Home route
@app.route('/home')
def home():
    customer = Customer.query.first()
    return render_template('index.html', customer=customer)

# Saldo route
@app.route('/saldo')
def saldo():
    customer = Customer.query.first()
    accounts = PortfolioAccount.query.filter_by(m_customer_id=customer.id).all()
    transactions = Transaction.query.filter_by(m_customer_id=customer.id).all()
    return render_template('saldo.html', customer=customer, accounts=accounts, transactions=transactions)

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')

@app.route('/input_saldo', methods=['GET', 'POST'])
def input_saldo():
    if request.method == 'POST':
        account_number = request.form['account_number']
        account_type = request.form['account_type']
        currency_code = request.form['currency_code']
        available_balance = request.form['available_balance']
        
        # Convert the input balance to a Decimal
        available_balance_decimal = Decimal(available_balance)
        
        # Find the account by account number
        account = PortfolioAccount.query.filter_by(account_number=account_number, account_type=account_type).first()
        
        if account:
            # Ensure account available balance is Decimal and update it
            account.available_balance = account.available_balance + available_balance_decimal

            # Create a new transaction for the saldo input with status 'SUCCESS'
            transaction = Transaction(
                m_customer_id=account.m_customer_id,
                transaction_type='CR',  # 'CR' for credit (incoming funds)
                transaction_amount=available_balance_decimal,
                transaction_date=datetime.now(pytz.timezone('Asia/Jakarta')),
                description=f'Input saldo to account {account_number}',
                status='SUCCESS'  # Set status to 'SUCCESS'
            )

            try:
                db.session.add(transaction)  # Add the transaction to the session
                db.session.commit()  # Commit both the balance update and the transaction

                flash(f'Successfully added {available_balance} to account {account_number}', 'success')
                return redirect(url_for('saldo'))  # Redirect to saldo view
            except Exception as e:
                db.session.rollback()  # Rollback in case of error
                flash(f'Error: {str(e)}', 'danger')
        else:
            flash(f'Account not found with account number {account_number}', 'danger')

    return render_template('input_saldo.html')

#API Model for Mobile Request

# Route untuk mendapatkan saldo dalam bentuk JSON
@app.route('/api/saldo', methods=['GET'])
def api_saldo():
    customer = Customer.query.first()
    accounts = PortfolioAccount.query.filter_by(m_customer_id=customer.id).all()
    transactions = Transaction.query.filter_by(m_customer_id=customer.id).all()

    accounts_data = []
    for account in accounts:
        accounts_data.append({
            'account_number': account.account_number,
            'available_balance': float(account.available_balance),  # Convert Decimal to float
            'account_name': account.account_name
        })

    transactions_data = []
    for transaction in transactions:
        transactions_data.append({
            'transaction_type': transaction.transaction_type,
            'transaction_amount': float(transaction.transaction_amount),
            'description': transaction.description,
            'transaction_date': transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({
        'customer_name': customer.customer_name,
        'accounts': accounts_data,
        'transactions': transactions_data
    })

# Route untuk melakukan transfer
@app.route('/api/transfer', methods=['POST'])
def api_transfer():
    data = request.get_json()
    account_number = data['account_number']
    amount = Decimal(data['amount'])

    account = PortfolioAccount.query.filter_by(account_number=account_number).first()

    if account and account.available_balance >= amount:
        # Update balance
        account.available_balance -= amount

        # Create transaction
        transaction = Transaction(
            m_customer_id=account.m_customer_id,
            transaction_type='DB',  # 'DB' for debit (outgoing funds)
            transaction_amount=amount,
            transaction_date=datetime.now(pytz.timezone('Asia/Jakarta')),
            description=f'Transfer from account {account_number}',
            status='SUCCESS'
        )

        try:
            db.session.add(transaction)
            db.session.commit()

            return jsonify({'message': 'Transfer successful', 'status': 'SUCCESS'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error: {str(e)}', 'status': 'FAILED'}), 500
    else:
        return jsonify({'message': 'Insufficient balance or account not found', 'status': 'FAILED'}), 400

# Index route
@app.route('/')
def index():
    customer = Customer.query.first()
    return render_template('index.html', customer=customer)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
