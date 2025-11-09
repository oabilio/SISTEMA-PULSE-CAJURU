import logging
from threading import Thread

from controllers.app1_controller import app, socketio, start_mqtt_client
from utils.create_db import create_db
from utils.inserts import populate_db
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    
    with app.app_context():
        create_db(app) 
        try:
            log.info("Populando banco com dados simulados...")
            populate_db(
                app,
                num_pessoas=80,
                num_atividades=15,
                num_setores=10,
                num_pontos=400,
                num_movimentacoes=200
            )
            log.info("Banco populado com sucesso!")
        except Exception as e:
            log.error(f"Erro ao popular o banco: {e}")
    
    log.info("Iniciando o servidor Flask-SocketIO...")
    
    mqtt_thread = Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    socketio.run(app, 
                 host='0.0.0.0', 
                 port=8080, 
                 debug=True, 
                 allow_unsafe_werkzeug=True, 
                 use_reloader=False)