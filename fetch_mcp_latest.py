from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from datetime import time
from datetime import date

import scrapy
from scrapy import Selector

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options

import time
import os

import csv

download_dir = os.getcwd() + '/Downloads/'
before = os.listdir(download_dir)

fp = webdriver.FirefoxProfile()
options = Options()

fp.set_preference("browser.download.folderList", 2)
#fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", download_dir)
#fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

driver = webdriver.Firefox(options=options, firefox_profile=fp, executable_path='./geckodriver')
print('Opened browser.')

driver.get("https://seffaflik.epias.com.tr/transparency/piyasalar/gop/ptf.xhtml")
print('Opened page.')
time.sleep(5)
driver.find_element_by_xpath('/html/body/div[5]/form/div[2]/div/div/div/div[2]/a[2]').click()
print('Downloaded file.')

after = os.listdir(download_dir)
change = set(after) - set(before)

if len(change) == 1:
    file_name = change.pop()
    print("New file:", file_name)
else:
    print("More than one file or no file downloaded")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MCPBase.db'

db = SQLAlchemy(app)

class MCP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time_hour = db.Column(db.Integer, nullable=False)
    price_tl = db.Column(db.Float, nullable=False)
    price_usd = db.Column(db.Float, nullable=False)
    price_eur = db.Column(db.Float, nullable=False)

with open(download_dir + file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            date_un_formatted = row[0].replace(' ', '')

            day = int(date_un_formatted[:2])
            month = int(date_un_formatted[3:-5])
            year = int(date_un_formatted[6:])

            date_to_add = date(year=year, month=month, day=day)

            hour = row[1].replace(' ', '')
            
            price_tl_temp = row[2].replace('.', '')
            price_usd_temp = row[3].replace('.', '')
            price_eur_temp = row[4].replace('.', '')

            price_tl = float(price_tl_temp.replace(',', '.'))
            price_usd = float(price_usd_temp.replace(',', '.'))
            price_eur = float(price_eur_temp.replace(',', '.'))

            new_mcp = MCP(date=date_to_add, time_hour=hour[:2], price_tl=price_tl, price_usd=price_usd, price_eur=price_eur)

            db.session.add(new_mcp)
            db.session.commit()

            line_count += 1

    total_count = str(line_count)
    print('Processed '+ total_count +  ' lines. - Inserted into DB!')




