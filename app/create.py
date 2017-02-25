from flask import render_template, redirect, url_for, request, g
from app import webapp

import mysql.connector

from app.config import db_config


def connect_to_database():
    return mysql.connector.connect(user=db_config['user'], 
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@webapp.route('/create',methods=['GET'])
#Display page for creating new account
def create():
	return render_template("create.html",title="Create New Account!")

@webapp.route('/create',methods=['POST'])
#Create a new account
def create_new():
	login = request.form.get('username', "")
	password = request.form.get('password', "")
	
	error = False
	
	if login == "" or password == "":
		error = True
	
	if error:
		return render_template("create.html", title="No empty user name or password allowed!")
	
	cnx = get_db()
	cursor = cnx.cursor()
	
	query = ''' INSERT INTO users (login, password) VALUES (%s, %s)'''
	
	cursor.execute(query, (login, password))
	cnx.commit()
	
	return redirect(url_for('main'))
