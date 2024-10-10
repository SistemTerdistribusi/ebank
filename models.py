from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class PortfolioAccount(db.Model):
    __tablename__ = 'm_portfolio_account'
    
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    m_customer_id = db.Column(db.BigInteger, db.ForeignKey('m_customer.id'))
    account_number = db.Column(db.String(20), nullable=True)
    account_name = db.Column(db.String(50), nullable=True)
    available_balance = db.Column(db.Numeric(30, 5), nullable=True)
    created = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    updated = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)

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
    
    # Relationship with portfolio account
    accounts = db.relationship('PortfolioAccount', backref='customer', lazy=True)

    def get_id(self):
        return self.id
