from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

instance = "mysql+pymysql://root:1234@localhost:3306/pulse_db"