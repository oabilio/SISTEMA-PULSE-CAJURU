# controllers/app_controller.py
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required
from controllers.login_controller import login_bp, User
from models.db import db, instance
from data import users

def create_app():
    app = Flask(__name__,
                template_folder="./views/",
                static_folder="./static/",
                root_path="./")

    app.secret_key = 'chave_super_secreta_e_segura'

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.index'

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance

    db.init_app(app)

    app.register_blueprint(login_bp, url_prefix='/')

    @login_manager.user_loader
    def load_user(user_id):
        if user_id in users:
            return User(user_id)
        return None

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect('/login')

    @app.route('/')
    def root():
        return redirect('/login')

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html')

    return app
