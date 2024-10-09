from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Account model
class Account(db.Model):
    __tablename__ = 'm_portofolio_account'

    id = db.Column(db.biginit, primary_key=True)
    account_number = db.Column(db.varchar(20), nullable=False)
    account_type = db.Column(db.varchar(10), nullable=False)
    currency_code = db.Column(db.char(3), nullable=False)
    available_balance = db.Column(db.decimal(30,5), nullable=False)

    def __init__(self, no_rekening, type_akun, mata_uang, available_balance):
        self.account_number = no_rekening
        self.account_type = type_akun
        self.currency_code = mata_uang
        self.available_balance = available_balance

# Create the tables in the database
with app.app_context():
    db.create_all()

@app.route('/input-saldo', methods=['GET'])
def input_saldo():
    return render_template('input_saldo.html')

@app.route('/process-saldo', methods=['POST'])
def process_saldo():
    no_rekening = request.form['account_number']
    type_akun = request.form['account_type']
    mata_uang = request.form['currency_code']
    available_balance = float(request.form['available_balance'])

    # Create a new account instance
    new_account = Account(account_number=no_rekening, account_type=type_akun, currency_code=mata_uang, available_balance=available_balance)

    # Add to the database session and commit
    db.session.add(new_account)
    db.session.commit()

    return redirect(url_for('input_saldo'))

if __name__ == '__main__':
    app.run(debug=True)
