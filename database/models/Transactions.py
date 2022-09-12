from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(80), unique=True, nullable=False)
    transaction_type = db.Column(db.String(30), unique=False, nullable=False)
    parent_id = db.Column(db.Integer, nullable=True)
