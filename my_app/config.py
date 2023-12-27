import os

PROPAGATE_EXCEPTIONS = True
FLASK_DEBUG = True
# SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}/{os.environ["POSTGRES_DB"]}'
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:3228@postgres:5432/mydb'
SQLALCHEMY_DATABASE_URI = 'postgresql://mydb_0nle_user:nHUxDpnvNxEIldD4WLuB6rhpP1BoU3uF@dpg-cm5jjf21hbls73ak45d0-a.oregon-postgres.render.com/mydb_0nle'

SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY='284311226774819625296707370484749044026'