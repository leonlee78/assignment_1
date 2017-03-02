from flask import redirect, url_for, request, g
import mysql.connector
from app import webapp
from app.config import db_config

class Database:
  def connect_to_database(self):
    return mysql.connector.connect(user=db_config['user'], 
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

  def get_db(self):
      db = getattr(g, '_database', None)
      if db is None:
          db = g._database = self.connect_to_database()
      return db

  @webapp.teardown_appcontext
  def teardown_db(exception):
      db = getattr(g, '_database', None)
      if db is not None:
          db.close()

  @webapp.teardown_appcontext
  def close_db(error):
      """Closes the database again at the end of the request."""
      if hasattr(g, 'sqlite_db'):
          g.sqlite_db.close()
