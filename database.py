from sqlalchemy.orm import sessionmaker, scoped_session
from dictalchemy import DictableModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, and_
from flask import Flask
import sys
import string
import random



class database_query:
    '''class to perform database queries'''
    def __init__(self,engine,Session_db):
        self.engine = engine
        self.Session_db = Session_db

    def select(self,table,filter_params=None):
        '''function to query the rows in table with where condition as filter_params'''
        try:
            with self.Session_db() as db_session:
                where_clauses = [getattr(table, column) == filter_params[column] for column in filter_params]
                result = db_session.query(table).where(and_(*where_clauses)).first()
                return result
        except Exception as e_:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print({"message": "exception in select " + str(e_) + ' ' + str(exc_tb.tb_lineno)})

    def insert(self, table, insert_params=None):
        ''' function to insert into the database with parameters inside insert_params as dictionary'''
        try:
            table_object = table(**insert_params)
            with self.Session_db() as db_session:
                db_session.add(table_object)
                db_session.commit()
                return table_object.id
        except Exception as e_:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print({"message": "exception in insert " + str(e_) + ' ' + str(exc_tb.tb_lineno)})
    def update(self, table, update_params=None, filter_params=None):
        ''' function to update into the database with parameters inside update_params as dictionary along with where condition as filter_params which is also a dictionary'''
        try:
            with self.Session_db() as db_session:
                where_clauses = [getattr(table, column) == filter_params[column] for column in filter_params]
                x = db_session.query(table).where(and_(*where_clauses)).update(values=update_params)
                db_session.commit()
                return x
        except Exception as e_:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print({"message": "exception in update " + str(e_) + ' ' + str(exc_tb.tb_lineno)})

def db_connection():
    '''function to create database connection that return engine and session'''
    engine = create_engine("mysql://root@localhost/<your database>")
    Session_db = scoped_session(sessionmaker(engine))
    return engine, Session_db

engine, session = db_connection() # creating engine and session object of database

Base = declarative_base(cls=DictableModel)
Base.metadata.reflect(engine)  # reflecting table at once so that database tables are present within Metadata object

query = database_query(engine,session)

class Url(Base):
    '''class that maps to url table in database'''
    __table__ = Base.metadata.tables['url']


def initialize_app():
    '''function to initialize flask app'''
    app_ = Flask(__name__)
    return app_

def randomize():
    '''function that generates short url'''
    random_string = string.ascii_lowercase + str(random.randint(0,9)) + string.ascii_uppercase + str(random.randint(0,9))
    return ''.join(random.choice(random_string) for _ in range(5))