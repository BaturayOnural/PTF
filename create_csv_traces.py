from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from datetime import time
from datetime import date
from collections import namedtuple

import os
import csv
import csv
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MCPBase.db'

db = SQLAlchemy(app)

class MCP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    price_tl=db.Column(db.Float, nullable=False)
    price_usd=db.Column(db.Float, nullable=False)
    price_eur=db.Column(db.Float, nullable=False)

start_date = date(2013,12,12)
end_date =   date(2015,12,15)

rows = db.session.query(MCP).filter(MCP.date.between(start_date, end_date))

#################################  TL
fp = open('trace_tl.csv', 'w')
myFile=csv.writer(fp)
header = ["Date","TL"]
myFile.writerow(header)
for row in rows:
	date=row.date
	price=row.price_tl
	data = [date,price]
	myFile.writerow(data)
fp.close()
##################################  USD
fp = open('trace_usd.csv', 'w')
myFile=csv.writer(fp)
header = ["Date","USD"]
myFile.writerow(header)
for row in rows:
	date=row.date
	price=row.price_usd
	data = [date,price]
	myFile.writerow(data)
fp.close()	
#################################   EUR
fp = open('trace_eur.csv', 'w')
myFile=csv.writer(fp)
header = ["Date","EUR"]
myFile.writerow(header)
for row in rows:
	date=row.date
	price=row.price_eur
	data = [date,price]
	myFile.writerow(data)
fp.close()


