#__init__.py
from models.db import db
from models.user.pessoa import Pessoa
from models.user.endereco import Endereco
from models.user.usuarios import Usuario
from models.user.roles import Role
from models.voluntarios.voluntario import Voluntario
from models.voluntarios.atividade import Atividade
from models.voluntarios.movimentacao import Movimentacao
from models.voluntarios.ponto import Ponto
from models.voluntarios.setor import Setor
from models.voluntarios.registro_atividade import RegistroAtividade
from models.documentos.documentacao import Documentacao
from models.documentos.doc1 import Doc1
from models.documentos.doc2 import Doc2
from models.documentos.doc3 import Doc3
from models.documentos.doc4 import Doc4
from models.documentos.pendencia import Pendencia