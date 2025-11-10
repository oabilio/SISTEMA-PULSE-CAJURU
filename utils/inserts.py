import random
from datetime import datetime, timedelta
from faker import Faker
from flask import Flask
from sqlalchemy.exc import IntegrityError

from models.db import db
from models.user.pessoa import Pessoa
from models.user.roles import Role
from models.user.usuarios import Usuario
from models.user.endereco import Endereco
from models.voluntarios.atividade import Atividade
from models.voluntarios.setor import Setor
from models.voluntarios.voluntario import Voluntario
from models.voluntarios.movimentacao import Movimentacao
from models.voluntarios.ponto import Ponto

faker = Faker('pt_BR')

def generate_random_date(start_date=datetime(2023, 1, 1), end_date=datetime.now()):
    return faker.date_time_between(start_date=start_date, end_date=end_date)

def populate_db(app: Flask, num_pessoas=50, num_atividades=10, num_setores=8, num_pontos=200, num_movimentacoes=100):
    
    with app.app_context():
        
        print("Iniciando a inserção de dados aleatórios...")
        
        pessoas_ids = []
        voluntarios_ids = []
        atividades_ids = []
        setores_ids = []
        
        # --- Pessoas ---
        print("Inserindo Pessoas...")
        for i in range(num_pessoas):
            try:
                nome = faker.name()
                pessoa = Pessoa(
                    nome=nome,
                    cpf=faker.cpf(),
                    telefone=faker.phone_number(),
                    data_nasc=faker.date_of_birth(minimum_age=18, maximum_age=70),
                    email=f"{nome.lower().replace(' ', '.')}.{i}@exemplo.com",
                    criado_em=generate_random_date(end_date=datetime(2023, 12, 31))
                )
                db.session.add(pessoa)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Aviso: Pulando pessoa {i} (CPF/Email duplicado).")
            except Exception as e:
                db.session.rollback()
                print(f"Aviso: Erro ao criar pessoa {i}: {e}. Pulando.")
        
        pessoas_ids = [p.id for p in Pessoa.query.all()]
        print(f"-> {len(pessoas_ids)} Pessoas inseridas/encontradas.")

        # --- Atividades ---
        print("Inserindo Atividades...")
        for _ in range(num_atividades):
            try:
                atividade = Atividade(
                    nome=faker.bs().capitalize(),
                    descricao=faker.text(max_nb_chars=100),
                    custo_hora=random.uniform(10.0, 50.0)
                )
                db.session.add(atividade)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print("Aviso: Pulando atividade (duplicada).")
            except Exception as e:
                db.session.rollback()
                print(f"Aviso: Erro ao criar atividade: {e}. Pulando.")

        atividades_ids = [a.id for a in Atividade.query.all()]
        print(f"-> {len(atividades_ids)} Atividades inseridas.")

        # --- Setores ---
        print("Inserindo Setores...")
        for _ in range(num_setores):
            try:
                setor = Setor(
                    nome=f"Setor {faker.word().capitalize()}",
                    descricao=faker.text(max_nb_chars=80)
                )
                db.session.add(setor)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print("Aviso: Pulando setor (duplicado).")
            except Exception as e:
                db.session.rollback()
                print(f"Aviso: Erro ao criar setor: {e}. Pulando.")
        
        setores_ids = [s.id for s in Setor.query.all()]
        print(f"-> {len(setores_ids)} Setores inseridos.")

        # --- Voluntários ---
        print("Inserindo Voluntários...")
        if pessoas_ids:
            pessoas_para_voluntarios_ids = random.sample(pessoas_ids, k=min(len(pessoas_ids), int(num_pessoas * 0.8)))
            for pessoa_id in pessoas_para_voluntarios_ids:
                try:
                    if not Voluntario.query.filter_by(pessoa_id=pessoa_id).first():
                        voluntario = Voluntario(
                            pessoa_id=pessoa_id,
                            codigo_rfid=f"0x{faker.hexify(text='^^*^^*^^*^^', upper=False)}",
                            status=random.choice(["ativo", "ativo", "ativo", "inativo"])
                        )
                        db.session.add(voluntario)
                        db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    print(f"Aviso: Pulando voluntário para pessoa {pessoa_id} (duplicado).")
                except Exception as e:
                    db.session.rollback()
                    print(f"Aviso: Erro ao criar voluntário para pessoa {pessoa_id}: {e}. Pulando.")
        
        todos_voluntarios = Voluntario.query.all()
        todas_atividades = Atividade.query.all()
        
        if todos_voluntarios and todas_atividades:
            print("Associando atividades a voluntários...")
            for vol in todos_voluntarios:
                try:
                    num_atividades_vol = random.randint(1, 3)
                    atividades_para_vol = random.sample(todas_atividades, k=num_atividades_vol)
                    for ativ in atividades_para_vol:
                        if ativ not in vol.atividades:
                            vol.atividades.append(ativ)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Erro ao associar atividades ao voluntário {vol.id}: {e}")

        voluntarios_ids = [v.id for v in todos_voluntarios]
        print(f"-> {len(voluntarios_ids)} Voluntários inseridos e associados.")

        # --- Pontos (Registros de Ponto) ---
        print("Inserindo Pontos...")
        if voluntarios_ids and atividades_ids:
            for _ in range(num_pontos):
                try:
                    entrada = generate_random_date()
                    duracao_horas = random.uniform(1, 5)
                    saida = entrada + timedelta(hours=duracao_horas)
                    
                    ponto = Ponto(
                        id_voluntario=random.choice(voluntarios_ids),
                        atividade_id=random.choice(atividades_ids),
                        entrada=entrada,
                        saida=saida,
                        origem=random.choice(["RFID", "Manual", "CPF"]),
                        observacao=faker.text(max_nb_chars=50) if random.random() > 0.8 else None
                    )
                    db.session.add(ponto)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Aviso: Erro ao criar ponto: {e}. Pulando.")
            print(f"-> {num_pontos} Registros de Ponto inseridos.")
        else:
            print("-> Pulando Pontos (sem voluntários ou atividades).")

        # --- Movimentações ---
        print("Inserindo Movimentações...")
        if voluntarios_ids and setores_ids:
            for _ in range(num_movimentacoes):
                try:
                    setores_sample = random.sample(setores_ids, k=2)
                    mov = Movimentacao(
                        solicitante=faker.name(),
                        paciente=faker.name(),
                        id_voluntario=random.choice(voluntarios_ids),
                        origem_id=setores_sample[0],
                        destino_id=setores_sample[1],
                        data=generate_random_date()
                    )
                    db.session.add(mov)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Aviso: Erro ao criar movimentação: {e}. Pulando.")
            print(f"-> {num_movimentacoes} Movimentações inseridas.")
        else:
            print("-> Pulando Movimentações (sem voluntários ou setores).")
            
        print("População do banco de dados concluída com sucesso!")