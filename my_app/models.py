from my_app.db import db

class CurrencyModel(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    
    user = db.relationship('UserModel', back_populates='currency')

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    default_currency_id = db.Column(db.String, db.ForeignKey('currency.id'), nullable=True)
    password = db.Column(db.String(128), nullable=False)

    currency = db.relationship('CurrencyModel', back_populates = 'user')
    record = db.relationship('RecordModel', back_populates = 'user')

class CategoryModel(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    record = db.relationship('RecordModel', back_populates='category')

class RecordModel(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.String, db.ForeignKey('category.id'), nullable=False)
    currency_id = db.Column(db.String, db.ForeignKey('currency.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    user = db.relationship('UserModel', back_populates='record')
    category = db.relationship('CategoryModel', back_populates = 'record')
    currency = db.relationship('CurrencyModel')

