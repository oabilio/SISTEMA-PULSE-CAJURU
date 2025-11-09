from flask import Flask, render_template, redirect, jsonify, request
from flask_login import LoginManager, login_required
from controllers.login_controller import login_bp
from controllers.pessoas_controller import pessoas_bp
from controllers.voluntarios_controller import voluntarios_bp
from controllers.atividades_controller import atividades_bp
from controllers.usuarios_controller import usuarios_bp
from controllers.ponto_controller import ponto_bp
from controllers.setores_controller import setores_bp
from controllers.movimentacoes_controller import movimentacoes_bp
from controllers.documentacoes_controller import documentacoes_bp
from controllers.pendencias_controller import pendencias_bp
from models.db import db, instance
from models.user.usuarios import Usuario

from models.voluntarios.voluntario import Voluntario
from models.voluntarios.atividade import Atividade
from models.voluntarios.setor import Setor
from models.voluntarios.movimentacao import Movimentacao
from models.voluntarios.ponto import Ponto
from sqlalchemy import func
from datetime import datetime, timedelta

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
    app.register_blueprint(documentacoes_bp, url_prefix="/")
    app.register_blueprint(pendencias_bp, url_prefix="/")

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
        
        date_str = request.args.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                target_date = datetime.utcnow().date()
        else:
            target_date = datetime.utcnow().date()
        
        target_date_str = target_date.isoformat()

        total_voluntarios_ativos = Voluntario.query.filter_by(status='ativo').count()
        atividades_ativas = Atividade.query.filter_by(ativo=True).count()

        pontos_fechados = Ponto.query.filter(Ponto.saida != None).all()
        total_duration = timedelta()
        for ponto in pontos_fechados:
            if ponto.duracao:
                total_duration += ponto.duracao
        total_horas = total_duration.total_seconds() / 3600
        total_horas_trabalhadas = "{:.1f}".format(total_horas)

        pontos_com_custo = db.session.query(Ponto, Atividade).join(Atividade, Ponto.atividade_id == Atividade.id).filter(Ponto.saida != None, Ponto.atividade_id != None).all()
        economia_total = 0.0
        for ponto, atividade in pontos_com_custo:
            if ponto.duracao and atividade.custo_hora:
                horas_ponto = ponto.duracao.total_seconds() / 3600
                economia_total += horas_ponto * float(atividade.custo_hora)
        economia_estimativa = "{:,.2f}".format(economia_total)

        setores_data_query = db.session.query(Setor.nome, func.count(Movimentacao.id))\
            .join(Setor, Movimentacao.destino_id == Setor.id)\
            .group_by(Setor.nome)\
            .order_by(func.count(Movimentacao.id).desc())\
            .all()
        
        setores_labels = [row[0] for row in setores_data_query]
        setores_data = [row[1] for row in setores_data_query]

        dias_labels = []
        dias_data = []
        today_for_chart = datetime.utcnow().date()
        for i in range(6, -1, -1):
            date_to_check = today_for_chart - timedelta(days=i)
            dias_labels.append(date_to_check.strftime('%d/%m'))
            count = Ponto.query.filter(func.date(Ponto.entrada) == date_to_check).count()
            dias_data.append(count)
        
        voluntarios_trabalhando_agora = Ponto.query.filter(Ponto.saida == None).count()
        entradas_do_dia = Ponto.query.filter(func.date(Ponto.entrada) == target_date).count()
        saidas_do_dia = Ponto.query.filter(func.date(Ponto.saida) == target_date).count()

        return render_template(
            'home.html',
            total_voluntarios_ativos=total_voluntarios_ativos,
            total_horas_trabalhadas=total_horas_trabalhadas,
            atividades_ativas=atividades_ativas,
            economia_estimativa=economia_estimativa,
            setores_labels=setores_labels,
            setores_data=setores_data,
            dias_labels=dias_labels,
            dias_data=dias_data,
            voluntarios_trabalhando_agora=voluntarios_trabalhando_agora,
            entradas_do_dia=entradas_do_dia,
            saidas_do_dia=saidas_do_dia,
            target_date_str=target_date_str
        )

    @app.route('/api/ponto_data')
    @login_required
    def api_ponto_data():
        dias_labels = []
        dias_data = []
        today = datetime.utcnow().date()
        for i in range(6, -1, -1):
            date_to_check = today - timedelta(days=i)
            dias_labels.append(date_to_check.strftime('%d/%m'))
            count = Ponto.query.filter(func.date(Ponto.entrada) == date_to_check).count()
            dias_data.append(count)
        
        return jsonify(
            dias_labels=dias_labels,
            dias_data=dias_data
        )

    return app