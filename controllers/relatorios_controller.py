import pandas as pd
import io
from flask import Blueprint, send_file, request, render_template
from flask_login import login_required
from models.db import db
from models.voluntarios.ponto import Ponto
from models.voluntarios.voluntario import Voluntario
from models.voluntarios.atividade import Atividade
from sqlalchemy import func, extract
from datetime import datetime

relatorios_bp = Blueprint("relatorios", __name__, template_folder="../views")

@relatorios_bp.route("/relatorios")
@login_required
def pagina_relatorios():
    hoje_str = datetime.utcnow().date().isoformat()
    return render_template("relatorios.html", hoje_str=hoje_str)

@relatorios_bp.route("/relatorio/dashboard_dia")
@login_required
def gerar_relatorio_dashboard_dia():
    
    date_str = request.args.get('date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = datetime.utcnow().date()
    else:
        target_date = datetime.utcnow().date()
    
    target_date_str = target_date.isoformat()

    kpis = db.session.query(
        func.count(Ponto.query.filter(Ponto.saida == None).subquery().c.id).label("trabalhando_agora"),
        func.count(Ponto.query.filter(func.date(Ponto.entrada) == target_date).subquery().c.id).label("entradas_dia"),
        func.count(Ponto.query.filter(func.date(Ponto.saida) == target_date).subquery().c.id).label("saidas_dia"),
        func.count(Voluntario.query.filter_by(status='ativo').subquery().c.id).label("voluntarios_ativos"),
        func.count(Atividade.query.filter_by(ativo=True).subquery().c.id).label("atividades_ativas")
    ).first()

    pontos_abertos_query = Ponto.query.filter(Ponto.saida == None).order_by(Ponto.entrada.desc()).all()
    
    df_kpis = pd.DataFrame({
        "Métrica": [
            "Trabalhando Agora", 
            f"Entradas em {target_date_str}", 
            f"Saídas em {target_date_str}",
            "Total Voluntários Ativos",
            "Total Atividades Ativas"
        ],
        "Valor": [
            kpis.trabalhando_agora,
            kpis.entradas_dia,
            kpis.saidas_dia,
            kpis.voluntarios_ativos,
            kpis.atividades_ativas
        ]
    })

    data_trabalhando = [{
        "Voluntário": p.voluntario.pessoa.nome,
        "Entrada": p.entrada.strftime('%Y-%m-%d %H:%M:%S'),
        "Origem": p.origem
    } for p in pontos_abertos_query]
    df_trabalhando = pd.DataFrame(data_trabalhando)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_kpis.to_excel(writer, sheet_name='Resumo_Dashboard_Dia', index=False)
        df_trabalhando.to_excel(writer, sheet_name='Trabalhando_Agora', index=False)
    
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'relatorio_pulse_dia_{target_date_str}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


def _get_pivot_table_df(agg_column, agg_func):
    
    if agg_column == 'horas':
        query_data = db.session.query(
            Atividade.nome.label('Atividade'),
            Ponto.entrada,
            Ponto.saida,
            Ponto.duracao
        ).join(Atividade).filter(Ponto.saida != None).all()
        
        df_raw = pd.DataFrame(query_data)
        if df_raw.empty:
            return pd.DataFrame(columns=["Atividade"])
            
        df_raw['Horas'] = df_raw['duracao'].dt.total_seconds() / 3600
        df_raw['Mes'] = df_raw['entrada'].dt.month
        df_raw['Ano'] = df_raw['entrada'].dt.year
        
        pivot = pd.pivot_table(
            df_raw,
            values='Horas',
            index='Atividade',
            columns=['Ano', 'Mes'],
            aggfunc=agg_func,
            fill_value=0,
            margins=True,
            margins_name="Total Geral"
        )
    else:
        query_data = db.session.query(
            Atividade.nome.label('Atividade'),
            extract('month', Ponto.entrada).label('Mes'),
            extract('year', Ponto.entrada).label('Ano'),
            func.count(Ponto.id).label('Contagem')
        ).join(Atividade).filter(Ponto.saida != None)\
         .group_by('Atividade', 'Ano', 'Mes')\
         .order_by('Ano', 'Mes', 'Atividade').all()
        
        df_raw = pd.DataFrame(query_data)
        if df_raw.empty:
            return pd.DataFrame(columns=["Atividade"])
            
        pivot = pd.pivot_table(
            df_raw,
            values='Contagem',
            index='Atividade',
            columns=['Ano', 'Mes'],
            aggfunc=agg_func,
            fill_value=0,
            margins=True,
            margins_name="Total Geral"
        )
    
    return pivot

def _get_indicadores_voluntarios_df():
    entradas_query = db.session.query(
        extract('year', Voluntario.data_entrada).label('Ano'),
        extract('month', Voluntario.data_entrada).label('Mes'),
        func.count(Voluntario.id).label('Voluntários que Entraram')
    ).group_by('Ano', 'Mes').order_by('Ano', 'Mes')
    
    df_entradas = pd.DataFrame(entradas_query.all())

    atuantes_query = db.session.query(
        extract('year', Ponto.entrada).label('Ano'),
        extract('month', Ponto.entrada).label('Mes'),
        func.count(func.distinct(Ponto.id_voluntario)).label('Voluntários Atuantes')
    ).filter(Ponto.saida != None).group_by('Ano', 'Mes').order_by('Ano', 'Mes')
    
    df_atuantes = pd.DataFrame(atuantes_query.all())

    all_entries = db.session.query(Voluntario.data_entrada).all()
    if not all_entries:
        df_geral_final = pd.DataFrame(columns=['Ano', 'Mes'])
    else:
        df_all_entries = pd.DataFrame(all_entries, columns=['data_entrada'])
        df_all_entries['data_entrada'] = pd.to_datetime(df_all_entries['data_entrada'])
        df_all_entries = df_all_entries.set_index('data_entrada').assign(count=1)
        df_cumulative = df_all_entries.resample('ME').sum().cumsum()
        df_cumulative = df_cumulative.rename(columns={'count': 'Total de Voluntários (Acumulado)'})
        df_cumulative['Ano'] = df_cumulative.index.year
        df_cumulative['Mes'] = df_cumulative.index.month
        
        df_geral = pd.merge(df_entradas, df_atuantes, on=['Ano', 'Mes'], how='outer')
        df_geral_final = pd.merge(df_geral, df_cumulative.reset_index(drop=True), on=['Ano', 'Mes'], how='outer')
        df_geral_final = df_geral_final.fillna(0)
    
    try:
        df_geral_pivot = df_geral_final.set_index(['Ano', 'Mes']).T
    except KeyError:
        return pd.DataFrame(columns=["Indicador"])
    
    return df_geral_pivot

@relatorios_bp.route("/relatorio/completo_mensal")
@login_required
def gerar_relatorio_completo_mensal():
    
    df_contagem = _get_pivot_table_df(agg_column='contagem', agg_func='sum')
    df_horas = _get_pivot_table_df(agg_column='horas', agg_func='sum')
    df_indicadores_vol = _get_indicadores_voluntarios_df()

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_contagem.to_excel(writer, sheet_name='Contagem por Atividade')
        df_horas.to_excel(writer, sheet_name='Horas por Atividade')
        df_indicadores_vol.to_excel(writer, sheet_name='Indicadores Voluntarios')
    
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'relatorio_pulse_completo_mensal.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )