from flask import Flask
from .main import main as main_bp
from .admin import admin as admin_bp
from .extensions import db, login_manager
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("app.instance_path:", app.instance_path)
    print("app.root_path:", app.root_path)

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Garante que as tabelas existem
    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')


    return app