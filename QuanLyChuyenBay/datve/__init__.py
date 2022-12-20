from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '$%^*&())(*&%^%4678675446&#%$%^&&*^$&%&*^&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/quanlyvemaybay?charset=utf8mb4' % quote(
    'Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name='QUẢN TRỊ BÁN VÉ', template_mode='bootstrap4')

login = LoginManager(app=app)
