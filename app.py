from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz

# Initialize Flask app
app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ebanking:hexagon123@panel.honjo.web.id:3306/ebanking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'wibunyel'

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

    def get_id(self):
        return self.id

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

# Initialize the database
@app.route('/initdb')
def initdb():
    db.create_all()

    # Create an honjo customer if it doesn't exist
    if not Customer.query.filter_by(customer_username='honjo').first():
        hashed_pin = generate_password_hash('123456', method='pbkdf2:sha256')
        new_customer = Customer(
            customer_username='honjo',
            customer_pin=hashed_pin,
            customer_name='Admin Honjo'
        )
        db.session.add(new_customer)
        db.session.commit()

    return 'Database initialized!'

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to index if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        
        customer = Customer.query.filter_by(customer_username=username).first()
        
        if customer and check_password_hash(customer.customer_pin, pin):
            login_user(customer)
            return redirect(url_for('index'))  # Redirect to the index page after login
        else:
            flash('Login failed. Check your username and PIN.')

    return render_template('login.html')

# Home route
@app.route('/home')
def home():
    return render_template('index.html', customer=current_user)

# Transfer route
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        # Handle transfer logic here
        # Example: Get transfer details from the form and process the transaction
        recipient_username = request.form.get('recipient_username')
        amount = request.form.get('amount')
        # Add your transfer logic here
        flash('Transfer successful!')
        return redirect(url_for('home'))
    
    return render_template('transfer.html')

# Saldo route
@app.route('/saldo')
def saldo():
    # Add logic to retrieve and display the user's balance
    return render_template('saldo.html', customer=current_user)

@app.route('/input_saldo')
def input_saldo():
    # no_rekening = request.form['no_rekening']
    # type_akun = request.form['type_akun']
    # mata_uang = request.form['mata_uang']
    # available_balance = request.form['available_balance']
    
    # You can process and save this data as needed
    # For example, saving to a database

    return render_template('input_saldo.html')

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run()
