# controllers/app_controller.py
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required
from controllers.login_controller import login_bp
from controllers.pessoas_controller import pessoas_bp
from controllers.voluntarios_controller import voluntarios_bp
from controllers.atividades_controller import atividades_bp
from controllers.usuarios_controller import usuarios_bp
from controllers.ponto_controller import ponto_bp
from controllers.setores_controller import setores_bp
from controllers.movimentacoes_controller import movimentacoes_bp
from models.db import db, instance
from models.user.usuarios import Usuario

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
    app.register_blueprint(pessoas_bp, url_prefix='/')
    app.register_blueprint(atividades_bp, url_prefix='/')
    app.register_blueprint(voluntarios_bp, url_prefix='/')
    app.register_blueprint(usuarios_bp, url_prefix='/')
    app.register_blueprint(ponto_bp, url_prefix="/")
    app.register_blueprint(setores_bp, url_prefix="/")
    app.register_blueprint(movimentacoes_bp, url_prefix="/")

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

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
