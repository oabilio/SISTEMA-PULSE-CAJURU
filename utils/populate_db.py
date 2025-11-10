from flask import Flask
from models.db import db
from datetime import datetime, timedelta
import random
from models.voluntarios.atividade import Atividade
from models.voluntarios.setor import Setor
from models.user.pessoa import Pessoa
from models.voluntarios.voluntario import Voluntario
from models.voluntarios.voluntario_atividade import voluntario_atividade_association
from models.voluntarios.ponto import Ponto
from models.voluntarios.movimentacao import Movimentacao

def populate_db(app: Flask):
    with app.app_context():
        db.session.add(Atividade(
            nome="Atendimento Telefônico",
            descricao="Atendimento receptivo e direcionamento de ligações aos setores do hospital.",
            custo_hora=5.00
        ))
        db.session.add(Atividade(
            nome="Acolhida no Internamento",
            descricao="Recepção e orientação de pacientes no momento da internação, oferecendo acolhimento humanizado.",
            custo_hora=6.00
        ))
        db.session.add(Atividade(
            nome="Acompanhamento Solidário",
            descricao="Presença e escuta ativa para pacientes e familiares em momentos de fragilidade.",
            custo_hora=6.50
        ))
        db.session.add(Atividade(
            nome="Visita Solidária",
            descricao="Visitas aos leitos com o objetivo de oferecer conforto emocional e apoio afetivo.",
            custo_hora=6.00
        ))
        db.session.add(Atividade(
            nome="Acolhimento Espiritual",
            descricao="Apoio espiritual respeitando as crenças e valores de cada paciente.",
            custo_hora=5.50
        ))
        db.session.add(Atividade(
            nome="Acolhimento Familiar HMC UTI 1",
            descricao="Apoio e acolhimento a familiares de pacientes internados na UTI 1 do Hospital Marcelino Champagnat.",
            custo_hora=7.00
        ))
        db.session.add(Atividade(
            nome="Acolhimento Familiar HMC UTI 2",
            descricao="Apoio e acolhimento a familiares de pacientes internados na UTI 2 do Hospital Marcelino Champagnat.",
            custo_hora=7.00
        ))
        db.session.add(Atividade(
            nome="Acolhimento Familiar HMC UTI 3",
            descricao="Apoio e acolhimento a familiares de pacientes internados na UTI 3 do Hospital Marcelino Champagnat.",
            custo_hora=7.00
        ))
        db.session.add(Atividade(
            nome="Acolhimento Familiar HMC UTI 4",
            descricao="Apoio e acolhimento a familiares de pacientes internados na UTI 4 do Hospital Marcelino Champagnat.",
            custo_hora=7.00
        ))
        db.session.add(Atividade(
            nome="Acolhimento Familiar HUC UTI 1",
            descricao="Acolhimento e suporte emocional a familiares de pacientes da UTI 1 do Hospital Universitário Cajuru.",
            custo_hora=6.50
        ))
        db.session.add(Atividade(
            nome="Acolhimento Familiar HUC UTI 2",
            descricao="Acolhimento e suporte emocional a familiares de pacientes da UTI 2 do Hospital Universitário Cajuru.",
            custo_hora=6.50
        ))
        db.session.add(Atividade(
            nome="Acolhimento Familiar HUC UTI 3",
            descricao="Acolhimento e suporte emocional a familiares de pacientes da UTI 3 do Hospital Universitário Cajuru.",
            custo_hora=6.50
        ))
        db.session.add(Atividade(
            nome="Anjos Solidários",
            descricao="Voluntários que levam mensagens e gestos de carinho aos pacientes internados.",
            custo_hora=5.50
        ))
        db.session.add(Atividade(
            nome="Contadores de Estória",
            descricao="Voluntários que narram histórias e promovem momentos lúdicos e de distração nos leitos.",
            custo_hora=4.50
        ))
        db.session.add(Atividade(
            nome="Origames do Bem",
            descricao="Confecção e entrega de origamis como gesto de carinho e arte terapêutica.",
            custo_hora=3.50
        ))
        db.session.add(Atividade(
            nome="Momento da Beleza",
            descricao="Atividade de cuidado pessoal e autoestima voltada a pacientes e acompanhantes.",
            custo_hora=5.00
        ))
        db.session.add(Atividade(
            nome="Auxílio Alimentação",
            descricao="Apoio voluntário na organização e entrega de refeições em setores específicos.",
            custo_hora=4.50
        ))
        db.session.add(Atividade(
            nome="Cuidando de Quem Cuida",
            descricao="Atividades de acolhimento, relaxamento e escuta para os profissionais de saúde.",
            custo_hora=6.00
        ))
        db.session.add(Atividade(
            nome="Auriculoterapia",
            descricao="Aplicação da técnica terapêutica de auriculoterapia para relaxamento e bem-estar.",
            custo_hora=7.50
        ))
        db.session.add(Atividade(
            nome="Reiki",
            descricao="Aplicação da técnica de Reiki, promovendo equilíbrio energético e relaxamento.",
            custo_hora=7.50
        ))
        db.session.add(Atividade(
            nome="Momento Musical",
            descricao="Apresentações musicais realizadas por voluntários em enfermarias e setores.",
            custo_hora=5.50
        ))
        db.session.add(Atividade(
            nome="Projeto Amigo Bicho",
            descricao="Visitas terapêuticas com animais de estimação, promovendo alegria e conforto emocional.",
            custo_hora=6.50
        ))

        db.session.commit()
        print("24 atividades inseridas.")

        setor1 = Setor(nome="Recepção Principal", descricao="Área de entrada e atendimento inicial aos pacientes e visitantes, localizada no térreo.")
        setor2 = Setor(nome="Pronto Atendimento", descricao="Setor destinado a casos de urgência e emergência médica, próximo à entrada principal de ambulâncias.")
        setor3 = Setor(nome="UTI 1", descricao="Unidade de Terapia Intensiva 1, equipada com leitos monitorados e suporte avançado à vida, localizada no 3º andar.")
        setor4 = Setor(nome="UTI 2", descricao="Unidade de Terapia Intensiva 2, voltada a pacientes críticos, situada no 3º andar, ala leste.")
        setor5 = Setor(nome="UTI 3", descricao="UTI voltada para cuidados intensivos pós-operatórios, no 4º andar.")
        setor6 = Setor(nome="UTI 4", descricao="Setor de terapia intensiva com foco em pacientes de longa permanência, localizado no 4º andar, ala norte.")
        setor7 = Setor(nome="Centro Cirúrgico", descricao="Área destinada à realização de procedimentos cirúrgicos, com salas esterilizadas e controle de acesso restrito.")
        setor8 = Setor(nome="Raio-X", descricao="Sala de diagnóstico por imagem, equipada com aparelhos de radiografia digital, localizada no 2º andar.")
        setor9 = Setor(nome="Tomografia", descricao="Setor com equipamentos de tomografia computadorizada de alta resolução, no 2º andar.")
        setor10 = Setor(nome="Laboratório de Análises Clínicas", descricao="Espaço destinado à coleta e processamento de amostras biológicas, localizado no 1º andar.")
        setor11 = Setor(nome="Farmácia Hospitalar", descricao="Responsável pela dispensação e controle de medicamentos, localizada próximo à UTI 1.")
        setor12 = Setor(nome="Enfermaria Feminina", descricao="Ala destinada à internação de pacientes do sexo feminino, no 2º andar.")
        setor13 = Setor(nome="Enfermaria Masculina", descricao="Ala de internação para pacientes do sexo masculino, localizada no 2º andar, ala norte.")
        setor14 = Setor(nome="Pediatria", descricao="Setor especializado em atendimento infantil, com ambiente lúdico e adaptado, no 1º andar.")
        setor15 = Setor(nome="Oncologia", descricao="Área voltada ao tratamento e acompanhamento de pacientes oncológicos, localizada no 5º andar.")
        setor16 = Setor(nome="Fisioterapia", descricao="Sala para sessões de fisioterapia e reabilitação motora, no 1º andar.")
        setor17 = Setor(nome="Psicologia", descricao="Ambiente reservado para atendimentos psicológicos individuais e em grupo, no 2º andar.")
        setor18 = Setor(nome="Nutrição", descricao="Sala destinada à equipe de nutrição e dietética, responsável pela elaboração de cardápios hospitalares.")
        setor19 = Setor(nome="Administração", descricao="Setor administrativo responsável pela gestão hospitalar, localizado no 6º andar.")
        setor20 = Setor(nome="Capela", descricao="Espaço de oração e acolhimento espiritual para pacientes, familiares e colaboradores.")
        setor21 = Setor(nome="Almoxarifado", descricao="Local de armazenamento de materiais hospitalares e insumos, no subsolo.")
        setor22 = Setor(nome="Manutenção", descricao="Área técnica responsável por reparos e manutenção predial, localizada nos fundos do hospital.")
        setor23 = Setor(nome="CME - Central de Materiais Esterilizados", descricao="Responsável pela limpeza, esterilização e distribuição de materiais cirúrgicos, no 1º andar.")
        setor24 = Setor(nome="Posto de Enfermagem 1", descricao="Estação de trabalho para equipe de enfermagem, localizada no corredor da ala leste do 2º andar.")
        setor25 = Setor(nome="Posto de Enfermagem 2", descricao="Estação de apoio para enfermeiros e técnicos, próxima aos quartos de internação no 3º andar.")

        db.session.add_all([
            setor1, setor2, setor3, setor4, setor5,
            setor6, setor7, setor8, setor9, setor10,
            setor11, setor12, setor13, setor14, setor15,
            setor16, setor17, setor18, setor19, setor20,
            setor21, setor22, setor23, setor24, setor25
        ])
        db.session.commit()
        print("25 setores inseridos")

        pessoa1 = Pessoa(nome="Ana Beatriz Silva", cpf="123.456.789-01", telefone="(41) 98812-3456", data_nasc="1996-05-10", email="ana.silva@gmail.com")
        pessoa2 = Pessoa(nome="Carlos Eduardo Souza", cpf="234.567.890-12", telefone="(41) 99745-8890", data_nasc="1987-03-22", email="carlos.souza@outlook.com")
        pessoa3 = Pessoa(nome="Fernanda Alves", cpf="345.678.901-23", telefone="(41) 99561-7823", data_nasc="1999-09-18", email="fernanda.alves@gmail.com")
        pessoa4 = Pessoa(nome="Rafael Oliveira", cpf="456.789.012-34", telefone="(41) 99845-1267", data_nasc="1991-07-14", email="rafael.oliveira@outlook.com")
        pessoa5 = Pessoa(nome="Juliana Santos", cpf="567.890.123-45", telefone="(41) 99672-4421", data_nasc="1984-11-09", email="juliana.santos@gmail.com")
        pessoa6 = Pessoa(nome="Marcos Paulo Ferreira", cpf="678.901.234-56", telefone="(41) 99455-7788", data_nasc="1975-08-27", email="marcos.ferreira@outlook.com")
        pessoa7 = Pessoa(nome="Camila Rocha", cpf="789.012.345-67", telefone="(41) 99122-9988", data_nasc="1993-01-05", email="camila.rocha@gmail.com")
        pessoa8 = Pessoa(nome="Vinícius Andrade", cpf="890.123.456-78", telefone="(41) 99877-1122", data_nasc="1988-04-30", email="vinicius.andrade@outlook.com")
        pessoa9 = Pessoa(nome="Larissa Pereira", cpf="901.234.567-89", telefone="(41) 99234-7766", data_nasc="1998-02-12", email="larissa.pereira@gmail.com")
        pessoa10 = Pessoa(nome="Thiago Costa", cpf="012.345.678-90", telefone="(41) 99345-6677", data_nasc="1985-12-25", email="thiago.costa@outlook.com")
        pessoa11 = Pessoa(nome="Amanda Ribeiro", cpf="135.246.579-11", telefone="(41) 99888-2233", data_nasc="1994-10-08", email="amanda.ribeiro@gmail.com")
        pessoa12 = Pessoa(nome="Gabriel Nascimento", cpf="246.357.680-22", telefone="(41) 99111-3344", data_nasc="1992-07-16", email="gabriel.nascimento@outlook.com")
        pessoa13 = Pessoa(nome="Isabela Martins", cpf="357.468.791-33", telefone="(41) 99222-4455", data_nasc="2001-03-11", email="isabela.martins@gmail.com")
        pessoa14 = Pessoa(nome="Pedro Henrique Moraes", cpf="468.579.802-44", telefone="(41) 99777-5566", data_nasc="1983-09-05", email="pedro.moraes@outlook.com")
        pessoa15 = Pessoa(nome="Bruna Carvalho", cpf="579.680.913-55", telefone="(41) 99633-6677", data_nasc="1995-06-14", email="bruna.carvalho@gmail.com")
        pessoa16 = Pessoa(nome="Leonardo Almeida", cpf="680.791.024-66", telefone="(41) 99144-7788", data_nasc="1980-02-27", email="leonardo.almeida@outlook.com")
        pessoa17 = Pessoa(nome="Tatiane Lopes", cpf="791.802.135-77", telefone="(41) 99255-8899", data_nasc="1997-08-03", email="tatiane.lopes@gmail.com")
        pessoa18 = Pessoa(nome="Felipe Moreira", cpf="802.913.246-88", telefone="(41) 99466-9900", data_nasc="1990-11-29", email="felipe.moreira@outlook.com")
        pessoa19 = Pessoa(nome="Carolina Castro", cpf="913.024.357-99", telefone="(41) 99955-2233", data_nasc="1993-05-02", email="carolina.castro@gmail.com")
        pessoa20 = Pessoa(nome="Diego Azevedo", cpf="024.135.468-00", telefone="(41) 99866-3344", data_nasc="1986-09-21", email="diego.azevedo@outlook.com")
        pessoa21 = Pessoa(nome="Luana Fernandes", cpf="135.246.579-12", telefone="(41) 99177-4455", data_nasc="1999-02-18", email="luana.fernandes@gmail.com")
        pessoa22 = Pessoa(nome="Ricardo Gomes", cpf="246.357.680-23", telefone="(41) 99488-5566", data_nasc="1972-06-24", email="ricardo.gomes@outlook.com")
        pessoa23 = Pessoa(nome="Natália Duarte", cpf="357.468.791-34", telefone="(41) 99299-6677", data_nasc="1991-04-17", email="natalia.duarte@gmail.com")
        pessoa24 = Pessoa(nome="André Lima", cpf="468.579.802-45", telefone="(41) 99700-7788", data_nasc="1989-12-05", email="andre.lima@outlook.com")
        pessoa25 = Pessoa(nome="Patrícia Freitas", cpf="579.680.913-56", telefone="(41) 99511-8899", data_nasc="1984-03-28", email="patricia.freitas@gmail.com")
        pessoa26 = Pessoa(nome="Rodrigo Melo", cpf="680.791.024-67", telefone="(41) 99122-9900", data_nasc="1997-07-13", email="rodrigo.melo@outlook.com")
        pessoa27 = Pessoa(nome="Juliane Vieira", cpf="791.802.135-78", telefone="(41) 99233-1122", data_nasc="1996-10-08", email="juliane.vieira@gmail.com")
        pessoa28 = Pessoa(nome="Bruno Santana", cpf="802.913.246-89", telefone="(41) 99444-2233", data_nasc="1981-01-22", email="bruno.santana@outlook.com")
        pessoa29 = Pessoa(nome="Michele Teixeira", cpf="913.024.357-90", telefone="(41) 99955-3344", data_nasc="1995-09-17", email="michele.teixeira@gmail.com")
        pessoa30 = Pessoa(nome="Gustavo Pires", cpf="024.135.468-01", telefone="(41) 99866-4455", data_nasc="1990-12-11", email="gustavo.pires@outlook.com")
        pessoa31 = Pessoa(nome="Larissa Faria", cpf="135.246.579-13", telefone="(41) 99177-5566", data_nasc="1998-04-09", email="larissa.faria@gmail.com")
        pessoa32 = Pessoa(nome="Eduardo Mendes", cpf="246.357.680-24", telefone="(41) 99488-6677", data_nasc="1985-07-03", email="eduardo.mendes@outlook.com")
        pessoa33 = Pessoa(nome="Sabrina Rocha", cpf="357.468.791-35", telefone="(41) 99299-7788", data_nasc="1992-01-15", email="sabrina.rocha@gmail.com")
        pessoa34 = Pessoa(nome="Tiago Barros", cpf="468.579.802-46", telefone="(41) 99700-8899", data_nasc="1983-05-26", email="tiago.barros@outlook.com")
        pessoa35 = Pessoa(nome="Priscila Lopes", cpf="579.680.913-57", telefone="(41) 99511-9900", data_nasc="1999-06-01", email="priscila.lopes@gmail.com")
        pessoa36 = Pessoa(nome="Matheus Cunha", cpf="680.791.024-68", telefone="(41) 99122-1010", data_nasc="1991-09-28", email="matheus.cunha@outlook.com")
        pessoa37 = Pessoa(nome="Daniele Correia", cpf="791.802.135-79", telefone="(41) 99233-2121", data_nasc="1989-08-03", email="daniele.correia@gmail.com")
        pessoa38 = Pessoa(nome="Renato Cardoso", cpf="802.913.246-90", telefone="(41) 99444-3232", data_nasc="1982-10-19", email="renato.cardoso@outlook.com")
        pessoa39 = Pessoa(nome="Helena Batista", cpf="913.024.357-91", telefone="(41) 99955-4343", data_nasc="1993-12-02", email="helena.batista@gmail.com")
        pessoa40 = Pessoa(nome="Fábio Ribeiro", cpf="024.135.468-02", telefone="(41) 99866-5454", data_nasc="1986-11-14", email="fabio.ribeiro@outlook.com")
        pessoa41 = Pessoa(nome="Paula Moraes", cpf="135.246.579-14", telefone="(41) 99177-6565", data_nasc="1997-05-23", email="paula.moraes@gmail.com")
        pessoa42 = Pessoa(nome="Luciano Rezende", cpf="246.357.680-25", telefone="(41) 99488-7676", data_nasc="1980-01-29", email="luciano.rezende@outlook.com")
        pessoa43 = Pessoa(nome="Aline Neves", cpf="357.468.791-36", telefone="(41) 99299-8787", data_nasc="1994-02-06", email="aline.neves@gmail.com")
        pessoa44 = Pessoa(nome="João Victor Pacheco", cpf="468.579.802-47", telefone="(41) 99700-9898", data_nasc="1992-09-19", email="joao.pacheco@outlook.com")
        pessoa45 = Pessoa(nome="Tatiana Brito", cpf="579.680.913-58", telefone="(41) 99511-0909", data_nasc="1988-03-30", email="tatiana.brito@gmail.com")
        pessoa46 = Pessoa(nome="Lucas Monteiro", cpf="680.791.024-69", telefone="(41) 99122-2020", data_nasc="1996-07-11", email="lucas.monteiro@outlook.com")
        pessoa47 = Pessoa(nome="Mariana Rocha", cpf="791.802.135-80", telefone="(41) 99233-3030", data_nasc="1993-04-15", email="mariana.rocha@gmail.com")
        pessoa48 = Pessoa(nome="Alexandre Prado", cpf="802.913.246-91", telefone="(41) 99444-4040", data_nasc="1984-10-21", email="alexandre.prado@outlook.com")
        pessoa49 = Pessoa(nome="Simone Ferreira", cpf="913.024.357-92", telefone="(41) 99955-5050", data_nasc="1990-01-08", email="simone.ferreira@gmail.com")
        pessoa50 = Pessoa(nome="Caio Barros", cpf="024.135.468-03", telefone="(41) 99866-6060", data_nasc="1998-12-04", email="caio.barros@outlook.com")

        db.session.add_all([
            pessoa1, pessoa2, pessoa3, pessoa4, pessoa5,
            pessoa6, pessoa7, pessoa8, pessoa9, pessoa10,
            pessoa11, pessoa12, pessoa13, pessoa14, pessoa15,
            pessoa16, pessoa17, pessoa18, pessoa19, pessoa20,
            pessoa21, pessoa22, pessoa23, pessoa24, pessoa25,
            pessoa26, pessoa27, pessoa28, pessoa29, pessoa30,
            pessoa31, pessoa32, pessoa33, pessoa34, pessoa35,
            pessoa36, pessoa37, pessoa38, pessoa39, pessoa40,
            pessoa41, pessoa42, pessoa43, pessoa44, pessoa45,
            pessoa46, pessoa47, pessoa48, pessoa49, pessoa50
        ])
        db.session.commit()
        print("50 pessoas inseridas com sucesso!")

        v1 = Voluntario(pessoa_id=1, codigo_rfid="0x02320D84A1", data_entrada=datetime(2025, 8, 1), status="ativo")
        v2 = Voluntario(pessoa_id=2, codigo_rfid="0x02320D84A2", data_entrada=datetime(2025, 8, 2), status="ativo")
        v3 = Voluntario(pessoa_id=3, codigo_rfid="0x02320D84A3", data_entrada=datetime(2025, 8, 3), status="ativo")
        v4 = Voluntario(pessoa_id=4, codigo_rfid="0x02320D84A4", data_entrada=datetime(2025, 8, 4), status="ativo")
        v5 = Voluntario(pessoa_id=5, codigo_rfid="0x02320D84A5", data_entrada=datetime(2025, 8, 5), status="ativo")
        v6 = Voluntario(pessoa_id=6, codigo_rfid="0x02320D84A6", data_entrada=datetime(2025, 8, 6), status="ativo")
        v7 = Voluntario(pessoa_id=7, codigo_rfid="0x02320D84A7", data_entrada=datetime(2025, 8, 7), status="ativo")
        v8 = Voluntario(pessoa_id=8, codigo_rfid="0x02320D84A8", data_entrada=datetime(2025, 8, 8), status="ativo")
        v9 = Voluntario(pessoa_id=9, codigo_rfid="0x02320D84A9", data_entrada=datetime(2025, 8, 9), status="ativo")
        v10 = Voluntario(pessoa_id=10, codigo_rfid="0x02320D84AA", data_entrada=datetime(2025, 8, 10), status="ativo")
        v11 = Voluntario(pessoa_id=11, codigo_rfid="0x02320D84AB", data_entrada=datetime(2025, 8, 11), status="ativo")
        v12 = Voluntario(pessoa_id=12, codigo_rfid="0x02320D84AC", data_entrada=datetime(2025, 8, 13), status="ativo")
        v13 = Voluntario(pessoa_id=13, codigo_rfid="0x02320D84AD", data_entrada=datetime(2025, 8, 15), status="ativo")
        v14 = Voluntario(pessoa_id=14, codigo_rfid="0x02320D84AE", data_entrada=datetime(2025, 8, 17), status="ativo")
        v15 = Voluntario(pessoa_id=15, codigo_rfid="0x02320D84AF", data_entrada=datetime(2025, 8, 19), status="ativo")
        v16 = Voluntario(pessoa_id=16, codigo_rfid="0x02320D84B0", data_entrada=datetime(2025, 8, 21), status="ativo")
        v17 = Voluntario(pessoa_id=17, codigo_rfid="0x02320D84B1", data_entrada=datetime(2025, 8, 23), status="ativo")
        v18 = Voluntario(pessoa_id=18, codigo_rfid="0x02320D84B2", data_entrada=datetime(2025, 8, 25), status="ativo")
        v19 = Voluntario(pessoa_id=19, codigo_rfid="0x02320D84B3", data_entrada=datetime(2025, 8, 27), status="ativo")
        v20 = Voluntario(pessoa_id=20, codigo_rfid="0x02320D84B4", data_entrada=datetime(2025, 8, 29), status="ativo")
        v21 = Voluntario(pessoa_id=21, codigo_rfid="0x02320D84B5", data_entrada=datetime(2025, 9, 1), status="ativo")
        v22 = Voluntario(pessoa_id=22, codigo_rfid="0x02320D84B6", data_entrada=datetime(2025, 9, 3), status="ativo")
        v23 = Voluntario(pessoa_id=23, codigo_rfid="0x02320D84B7", data_entrada=datetime(2025, 9, 5), status="ativo")
        v24 = Voluntario(pessoa_id=24, codigo_rfid="0x02320D84B8", data_entrada=datetime(2025, 9, 7), status="ativo")
        v25 = Voluntario(pessoa_id=25, codigo_rfid="0x02320D84B9", data_entrada=datetime(2025, 9, 9), status="ativo")
        v26 = Voluntario(pessoa_id=26, codigo_rfid="0x02320D84BA", data_entrada=datetime(2025, 9, 11), status="ativo")
        v27 = Voluntario(pessoa_id=27, codigo_rfid="0x02320D84BB", data_entrada=datetime(2025, 9, 13), status="ativo")
        v28 = Voluntario(pessoa_id=28, codigo_rfid="0x02320D84BC", data_entrada=datetime(2025, 9, 15), status="ativo")
        v29 = Voluntario(pessoa_id=29, codigo_rfid="0x02320D84BD", data_entrada=datetime(2025, 9, 17), status="ativo")
        v30 = Voluntario(pessoa_id=30, codigo_rfid="0x02320D84BE", data_entrada=datetime(2025, 9, 19), status="ativo")
        v31 = Voluntario(pessoa_id=31, codigo_rfid="0x02320D84BF", data_entrada=datetime(2025, 9, 21), status="ativo")
        v32 = Voluntario(pessoa_id=32, codigo_rfid="0x02320D84C0", data_entrada=datetime(2025, 9, 23), status="ativo")
        v33 = Voluntario(pessoa_id=33, codigo_rfid="0x02320D84C1", data_entrada=datetime(2025, 9, 25), status="ativo")
        v34 = Voluntario(pessoa_id=34, codigo_rfid="0x02320D84C2", data_entrada=datetime(2025, 9, 27), status="ativo")
        v35 = Voluntario(pessoa_id=35, codigo_rfid="0x02320D84C3", data_entrada=datetime(2025, 9, 29), status="ativo")
        v36 = Voluntario(pessoa_id=36, codigo_rfid="0x02320D84C4", data_entrada=datetime(2025, 10, 1), status="ativo")
        v37 = Voluntario(pessoa_id=37, codigo_rfid="0x02320D84C5", data_entrada=datetime(2025, 10, 3), status="ativo")
        v38 = Voluntario(pessoa_id=38, codigo_rfid="0x02320D84C6", data_entrada=datetime(2025, 10, 5), status="ativo")
        v39 = Voluntario(pessoa_id=39, codigo_rfid="0x02320D84C7", data_entrada=datetime(2025, 10, 7), status="ativo")
        v40 = Voluntario(pessoa_id=40, codigo_rfid="0x02320D84C8", data_entrada=datetime(2025, 10, 9), status="ativo")
        v41 = Voluntario(pessoa_id=41, codigo_rfid="0x02320D84C9", data_entrada=datetime(2025, 10, 12), status="ativo")
        v42 = Voluntario(pessoa_id=42, codigo_rfid="0x02320D84CA", data_entrada=datetime(2025, 10, 15), status="ativo")
        v43 = Voluntario(pessoa_id=43, codigo_rfid="0x02320D84CB", data_entrada=datetime(2025, 10, 18), status="ativo")
        v44 = Voluntario(pessoa_id=44, codigo_rfid="0x02320D84CC", data_entrada=datetime(2025, 10, 21), status="ativo")
        v45 = Voluntario(pessoa_id=45, codigo_rfid="0x02320D84CD", data_entrada=datetime(2025, 10, 24), status="ativo")
        v46 = Voluntario(pessoa_id=46, codigo_rfid="0x02320D84CE", data_entrada=datetime(2025, 10, 27), status="ativo")
        v47 = Voluntario(pessoa_id=47, codigo_rfid="0x02320D84CF", data_entrada=datetime(2025, 10, 30), status="ativo")
        v48 = Voluntario(pessoa_id=48, codigo_rfid="0x02320D84D0", data_entrada=datetime(2025, 11, 3), status="ativo")
        v49 = Voluntario(pessoa_id=49, codigo_rfid="0x02320D84D1", data_entrada=datetime(2025, 11, 6), status="ativo")
        v50 = Voluntario(pessoa_id=50, codigo_rfid="0x02320D84D2", data_entrada=datetime(2025, 11, 9), status="ativo")

        db.session.add_all([
            v1, v2, v3, v4, v5, v6, v7, v8, v9, v10,
            v11, v12, v13, v14, v15, v16, v17, v18, v19, v20,
            v21, v22, v23, v24, v25, v26, v27, v28, v29, v30,
            v31, v32, v33, v34, v35, v36, v37, v38, v39, v40,
            v41, v42, v43, v44, v45, v46, v47, v48, v49, v50
        ])
        db.session.commit()
        print("50 voluntários inseridos com sucesso!")

        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=1, id_atividade=1))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=2, id_atividade=4))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=3, id_atividade=10))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=4, id_atividade=3))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=5, id_atividade=15))

        # Voluntários com 2 atividades
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=6, id_atividade=2))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=6, id_atividade=7))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=7, id_atividade=5))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=7, id_atividade=8))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=8, id_atividade=6))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=8, id_atividade=11))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=9, id_atividade=3))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=9, id_atividade=13))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=10, id_atividade=1))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=10, id_atividade=17))

        # Voluntários com 3 atividades
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=11, id_atividade=2))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=11, id_atividade=9))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=11, id_atividade=14))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=12, id_atividade=4))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=12, id_atividade=5))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=12, id_atividade=20))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=13, id_atividade=7))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=13, id_atividade=9))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=13, id_atividade=12))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=14, id_atividade=3))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=14, id_atividade=16))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=14, id_atividade=21))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=15, id_atividade=5))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=15, id_atividade=10))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=15, id_atividade=18))

        # Voluntários com 4 atividades
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=16, id_atividade=1))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=16, id_atividade=2))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=16, id_atividade=3))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=16, id_atividade=4))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=17, id_atividade=6))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=17, id_atividade=7))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=17, id_atividade=8))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=17, id_atividade=9))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=18, id_atividade=10))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=18, id_atividade=11))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=18, id_atividade=12))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=18, id_atividade=13))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=19, id_atividade=14))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=19, id_atividade=15))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=19, id_atividade=16))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=19, id_atividade=17))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=20, id_atividade=18))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=20, id_atividade=19))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=20, id_atividade=20))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=20, id_atividade=21))

        # Distribuindo o resto (21 a 50) variadamente
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=21, id_atividade=5))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=22, id_atividade=1))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=23, id_atividade=4))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=23, id_atividade=5))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=24, id_atividade=11))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=25, id_atividade=14))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=26, id_atividade=3))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=26, id_atividade=8))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=27, id_atividade=9))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=27, id_atividade=12))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=28, id_atividade=17))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=29, id_atividade=19))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=30, id_atividade=20))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=31, id_atividade=21))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=32, id_atividade=22))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=33, id_atividade=2))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=33, id_atividade=5))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=34, id_atividade=6))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=34, id_atividade=7))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=35, id_atividade=8))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=36, id_atividade=9))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=37, id_atividade=10))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=38, id_atividade=11))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=39, id_atividade=12))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=40, id_atividade=13))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=41, id_atividade=14))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=42, id_atividade=15))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=43, id_atividade=16))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=44, id_atividade=17))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=45, id_atividade=18))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=46, id_atividade=19))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=47, id_atividade=20))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=48, id_atividade=21))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=49, id_atividade=22))
        db.session.execute(voluntario_atividade_association.insert().values(id_voluntario=50, id_atividade=1))

        db.session.commit()
        print("Associações de voluntários e atividades inseridas com sucesso!")

        start_date = datetime(2025, 8, 4)
        end_date = datetime(2025, 11, 9)
        origens = ["Manual", "CPF", "RFID"]
        pontos = []

        current_date = start_date
        while current_date <= end_date:
            for i in range(15):  # 15 pontos por dia
                entrada_hour = random.choice(range(8, 19))  # 08h até 18h
                entrada = current_date.replace(hour=entrada_hour, minute=0)
                duracao = random.choice([1, 2, 3, 4])
                saida = entrada + timedelta(hours=duracao)

                origem = random.choice(origens)
                rfid = None
                if origem == "RFID":
                    rfid = f"0x02320D84{random.randint(10, 99)}"

                id_voluntario = random.randint(1, 50)
                atividade_id = random.randint(1, 22)

                ponto = Ponto(
                    entrada=entrada,
                    saida=saida,
                    origem=origem,
                    rfid=rfid,
                    id_voluntario=id_voluntario,
                    atividade_id=atividade_id
                )
                pontos.append(ponto)

            current_date += timedelta(days=1)

        db.session.add_all(pontos)
        db.session.commit()
        print(f"{len(pontos)} pontos inseridos de {start_date.date()} até {end_date.date()}.")

        p1 = Ponto(entrada=datetime(2025, 11, 10, 7, 0),  saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=1,  atividade_id=3)
        p2 = Ponto(entrada=datetime(2025, 11, 10, 7, 0),  saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=5,  atividade_id=7)
        p3 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=12, atividade_id=2)
        p4 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=18, atividade_id=9)
        p5 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=20, atividade_id=11)
        p6 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=23, atividade_id=5)
        p7 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=27, atividade_id=14)
        p8 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=30, atividade_id=6)
        p9 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=33, atividade_id=8)
        p10 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=36, atividade_id=12)
        p11 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=40, atividade_id=1)
        p12 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=42, atividade_id=20)
        p13 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=45, atividade_id=17)
        p14 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=48, atividade_id=22)
        p15 = Ponto(entrada=datetime(2025, 11, 10, 7, 0), saida=None, origem="Manual", observacao=None, rfid=None, id_voluntario=50, atividade_id=19)

        db.session.add_all([
            p1, p2, p3, p4, p5,
            p6, p7, p8, p9, p10,
            p11, p12, p13, p14, p15
        ])
        db.session.commit()
        print("15 pontos abertos inseridos.")

        start_date = datetime(2025, 8, 4)
        end_date = datetime(2025, 11, 9)

        nomes = [
            "Ana Silva", "Bruno Souza", "Carla Pereira", "Daniel Lima", "Eduardo Rocha",
            "Fernanda Alves", "Gabriel Costa", "Helena Martins", "Igor Ferreira", "Julia Gomes"
        ]

        current_date = start_date
        movimentacoes = []

        while current_date <= end_date:
            for _ in range(10):  # 10 movimentações por dia
                solicitante = random.choice(nomes)
                paciente = random.choice(nomes)
                while paciente == solicitante:  # evitar que seja a mesma pessoa
                    paciente = random.choice(nomes)

                id_voluntario = random.randint(1, 50)

                origem_id = random.randint(1, 25)
                destino_id = random.randint(1, 25)
                while destino_id == origem_id:
                    destino_id = random.randint(1, 25)

                movimentacao = Movimentacao(
                    solicitante=solicitante,
                    paciente=paciente,
                    id_voluntario=id_voluntario,
                    data=current_date.date(),
                    origem_id=origem_id,
                    destino_id=destino_id
                )
                movimentacoes.append(movimentacao)

            current_date += timedelta(days=1)

        db.session.add_all(movimentacoes)
        db.session.commit()
        print(f"{len(movimentacoes)} movimentações de acompanhamento solidário inseridas de {start_date.date()} até {end_date.date()}.")

