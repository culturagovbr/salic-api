# encoding: utf-8
# encoding: iso-8859-1

import sys
sys.path.append('../..')
from app import app
from sql_connector import SQL_connector
from sqlalchemy import create_engine, Column, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from flask import Flask
from utils.Log import Log
import urllib

import datetime, json



class MSSql_connector(SQL_connector):

    def __init__(self):

        if app.config['SQL_DRIVER'] == 'pymssql':
          engine = create_engine(r"mssql+pymssql://{0}:{1}@{2}:{3}/{4}".format(
                                          app.config['DATABASE_USER'],
                                          app.config['DATABASE_PASSWORD'],
                                          app.config['DATABASE_HOST'],
                                          app.config['DATABASE_PORT'],
                                          app.config['DATABASE_NAME']))

        else:
          quoted = urllib.quote_plus('DRIVER={FreeTDS};Server=%s;Database=%s;UID=%s;PWD=%s;TDS_Version=8.0;CHARSET=UTF8;Port=1433;'
                                          %(app.config['DATABASE_HOST'],
                                            app.config['DATABASE_NAME'],
                                            app.config['DATABASE_USER'],
                                            app.config['DATABASE_PASSWORD']))

          engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted), connect_args={'convert_unicode': True})

        # create a Session
        Session = sessionmaker(bind=engine)

        try:
            self.session = Session()
            event.listen(Session, "after_transaction_create", self.session.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED'))
            
            Log.info('Connection Openned')
        except:
            Log.info('Can\'t create database session')
            raise


    def __del__(self):
        # close session after query executes
        self.session.close()
        Log.info('Database connection closed')
