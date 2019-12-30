from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from datetime import time

import os
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MCPBase.db'

db = SQLAlchemy(app)

class MCP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False)
    time_hour = db.Column(db.Integer, nullable=False)
    price_tl = db.Column(db.Float, nullable=False)
    price_usd = db.Column(db.Float, nullable=False)
    price_eur = db.Column(db.Float, nullable=False)

db.create_all()

with open('PTF-31122019.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(''.join(row))
            line_count += 1
        else:
            date = row[0]
            hour = row[1]
            print(row[3])
            print(row[2])
            price_tl = float(row[2])
            price_usd = float(row[3])
            price_eur = float(row[4])

            date_formatted = 2

            new_mcp = MCP(date_created = datetime.now(), time_hour = hour[:2], price_tl=price_tl, price_usd=price_usd, price_eur=price_eur)

            db.session.add(new_mcp)
            db.session.commit()

            line_count += 1

    total_count = str(line_count)
    print('Processed '+ total_count +  ' lines.')