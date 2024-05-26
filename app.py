from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from app import auth, main
app.register_blueprint(auth.bp)
app.register_blueprint(main.bp)

if __name__ == '__main__':
    app.run(debug=True)
