from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from datetime import time
from datetime import date

import os
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MCPBase_TL.db'

db = SQLAlchemy(app)

class MCP(db.Model):
    symbol = db.Column(db.String, nullable=False, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, primary_key=True)
    price=db.Column(db.Float, nullable=False, primary_key=True)

db.create_all()

with open('PTF-04012020.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(''.join(row))
            line_count += 1
        else:
            date_un_formatted = row[0].replace(' ', '')

            day = int(date_un_formatted[:2])
            month = int(date_un_formatted[3:-5])
            year = int(date_un_formatted[6:])
          
            hour = row[1].replace(' ', '')

            # datetime(year, month, day, hour, minute, second, microsecond)
            date_formatted = datetime(year, month, day, int(hour[:2]), 00, 00, 00000)

            price_tl_temp = row[2].replace('.', '')
            price_usd_temp = row[3].replace('.', '')
            price_eur_temp = row[4].replace('.', '')

            price_tl = float(price_tl_temp.replace(',', '.'))
            price_usd = float(price_usd_temp.replace(',', '.'))
            price_eur = float(price_eur_temp.replace(',', '.'))

            new_mcp_tl = MCP(symbol="TL/MWh", date=date_formatted, price=price_tl)
            #new_mcp_usd = MCP(symbol="USD/MWh", date=date_formatted, price=price_usd)
            #new_mcp_eur = MCP(symbol="EUR/MWh", date=date_formatted, price=price_eur)

            db.session.add(new_mcp_tl)
            #db.session.add(new_mcp_usd)
            #db.session.add(new_mcp_eur)
            db.session.commit()

            line_count += 1

    total_count = str(line_count)
    print('Processed '+ total_count +  ' lines.')