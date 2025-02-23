from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Import main_bp after app is created to avoid circular import
from website.routes import main_bp
from website.dataReq import data_reqs_bp
from website.user_routes import user_bp
from website.notification import notification_bp

app.register_blueprint(main_bp)
app.register_blueprint(data_reqs_bp)
app.register_blueprint(user_bp)
app.register_blueprint(notification_bp) 