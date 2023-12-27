import uuid
from flask import request
from datetime import datetime
from marshmallow import ValidationError
from flask import Blueprint
from sqlalchemy.exc import IntegrityError

from .db import db
from .models import UserModel, CategoryModel, CurrencyModel, RecordModel
from .schemas import UserSchema, CategorySchema, CurrencySchema, RecordSchema

healthcheck_blueprint = Blueprint('healthcheck', __name__)
user_blueprint = Blueprint('user', __name__)
category_blueprint = Blueprint('category', __name__)
record_blueprint = Blueprint('record', __name__)
currency_blueprint = Blueprint('currency', __name__)

@healthcheck_blueprint.route('/healthcheck')
def healthcheck():
    current_time = datetime.now().isoformat()
    status = 'OK'

    response_data = {
        'status': status,
        'timestamp': current_time
    }

    return response_data, 200

@user_blueprint.get('/user/<user_id>')
def user_get(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return {'error': f'No user found with id {user_id}'}, 404
    try:
        return UserSchema().dump(user), 200
    except ValidationError as err:
        return err.messages, 400

@user_blueprint.delete('/user/<user_id>')
def user_delete(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return {'error': f'No user found with id {user_id}'}, 404
    try:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User with id {user_id} successfully deleted'}, 200
        # return UserSchema().dump(user), 200
    except ValidationError as err:   
        return err.messages, 400

@user_blueprint.post('/user')
def user_add():
    try:
        data = UserSchema().load(request.json)
    except ValidationError as err:
        return err.messages, 400
    data['id'] = uuid.uuid4().hex

    if 'default_currency_id' not in data or not data['default_currency_id']:
        uah_currency = CurrencyModel.query.filter_by(name='UAH').first()
        data['default_currency_id'] = uah_currency.id if uah_currency else None
    user = UserModel(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return e, 400
    return UserSchema().dump(user)

@user_blueprint.get('/users')
def users_get():
    all_users = UserModel.query.all()
    return UserSchema(many=True).dump(all_users)

@category_blueprint.get('/category')
def categories_get():
    all_categories = CategoryModel.query.all()
    return CategorySchema(many=True).dump(all_categories)

@category_blueprint.post('/category')
def category_add():
    try:
        data = CategorySchema().load(request.json)
    except ValidationError as err:
        return err.messages, 400
    data['id'] = uuid.uuid4().hex
    category = CategoryModel(**data)
    try:
        db.session.add(category)
        db.session.commit()
    except Exception as e:
        return e, 400
    return CategorySchema().dump(category)

@category_blueprint.delete('/category')
def category_delete():
    category_id = request.args.get('category_id')
    if not category_id:
        return {'error': 'Category id is required'}, 400
    
    category = CategoryModel.query.get(category_id)
    if not category:
        return {'error': f'No category found with id {category_id}'}, 404

    # db.session.delete(category)
    # db.session.commit()
    # return {'message': f'Category {category_id} deleted successfully'}
    try:
        db.session.delete(category)
        db.session.commit()
        return CategorySchema().dump(category), 200
    except ValidationError as err:   
        return err.messages, 400

@record_blueprint.get('/record/<record_id>')
def record_get(record_id):
    record = RecordModel.query.get(record_id)
    if not record:
        return {'error': f'No record found with id {record_id}'}, 404
    try:
        return RecordSchema().dump(record), 200
    except ValidationError as err:
        return err.messages, 400

@record_blueprint.delete('/record/<record_id>')
def record_delete(record_id):
    record = RecordModel.query.get(record_id)
    if not record:
        return {'error': f'No record found with id {record_id}'}, 404
    try:
        db.session.delete(record)
        db.session.commit()
        return RecordSchema().dump(record), 200
    except ValidationError as err:
        return err.messages

@record_blueprint.post('/record')
def record_add():
    try:
        data = RecordSchema().load(request.json)
    except ValidationError as err:
        return err.messages, 400
    # data = RecordSchema().load(request.json)
    data['id'] = uuid.uuid4().hex
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    user = UserModel.query.get(data['user_id'])
    category = CategoryModel.query.get(data['category_id'])

    if user and category:
        data['user_id'] = user.id
        if user.default_currency_id:
            data['currency_id'] = user.default_currency_id
        else:
            default_currency = CurrencyModel.query.filter_by(name='UAH').first()
            data['currency_id'] = default_currency.id if default_currency else None
        data['category_id'] = category.id
        record = RecordModel(**data)
    else:
        return {'error': 'Invalid data'}, 400
    try:
        db.session.add(record)
        db.session.commit()
        return RecordSchema().dump(record), 200
    except Exception as e:
        return e, 400

@record_blueprint.get('/record')
def records_get():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return {'error': 'At least one of User id or Category id is required'}, 400
    
    user = UserModel.query.get(user_id)
    category = CategoryModel.query.get(category_id)

    if user_id and not user:
        return {'error': 'User not found'}, 404
    if category_id and not category:
        return {'error': 'Category not found'}, 404
    
    query = RecordModel.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter_by(category_id=category_id)

    try:
        records = query.all()
    except Exception as e:
        return e, 400
    return RecordSchema(many=True).dump(records)

@currency_blueprint.get('/currency')
def currency_get():
    all_currencies = CurrencyModel.query.all()
    return CurrencySchema(many=True).dump(all_currencies)

@currency_blueprint.post('/currency')
def currency_add():
    try:
        data = CurrencySchema().load(request.json)
    except ValidationError as err:
        return err.messages
    data['id'] = uuid.uuid4().hex
    currency = CurrencyModel(**data)
    try:
        db.session.add(currency)
        db.session.commit()
        return CurrencySchema().dump(currency), 200
    except IntegrityError:
        return {'error': 'This currency already exists'}, 400
    
@currency_blueprint.delete('/currency/<currency_id>')
def currency_delete(currency_id):
    currency = CurrencyModel.query.get(currency_id)
    try:
        db.session.delete(currency)
        db.session.commit()
        return CurrencySchema().dump(currency), 200
    except ValidationError as err:
        return err.messages

