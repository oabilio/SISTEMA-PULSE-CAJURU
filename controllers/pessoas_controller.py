# controllers/pessoas_controller.py
from flask import Blueprint, request, render_template
from flask_login import login_required
from models.user.pessoa import Pessoa
from models.user.endereco import Endereco

pessoas_bp = Blueprint("pessoas", __name__, template_folder="../views")

@pessoas_bp.route('/cadastrar_pessoa')
@login_required
def cadastrar_pessoa():
    return render_template("cadastro_pessoa.html")

@pessoas_bp.route('/add_pessoa', methods=['POST'])
@login_required
def add_pessoa():
    nome = request.form.get("first_name")
    cpf = request.form.get("cpf")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    data_nasc = request.form.get("data_nasc")

    logradouro = request.form.get("logradouro")
    numero = request.form.get("numero")
    bairro = request.form.get("bairro")
    cidade = request.form.get("cidade")
    estado = request.form.get("estado")
    cep = request.form.get("cep")
    complemento = request.form.get("complemento")

    pessoa = Pessoa.save_pessoa(nome, cpf, telefone, data_nasc, email)
    Endereco.save_endereco(pessoa.id, logradouro, numero, bairro, cidade, estado, cep, complemento)
    
    return render_template("home.html")