from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/bookdb'   #pymysql is a driver base ahe means for communication purpose
app.config['SQLALCHEMY_ECHO']=True      # jo query sqlalchemy create kar raha hai ho sqlalchemy_echo ha python madhe console var print karun denar
db = SQLAlchemy(app)