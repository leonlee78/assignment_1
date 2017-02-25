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


@webapp.route('/login',methods=['POST'])
def login():
	login = request.form.get('username', "")
	password = request.form.get('password', "")
	
	#login = 'new'
	#password = 'new'
	
	cnx = get_db()
	
	cursor = cnx.cursor()
	
	query = ''' SELECT COUNT(1) FROM users WHERE login = %s '''
	
	cursor.execute(query, (login, ))
	
	row = cursor.fetchone()[0]
	
	if row:
		#login exists
		query = ''' SELECT * FROM users WHERE login = %s '''
		cursor.execute(query, (login, ))
		row = cursor.fetchone()
		userId = row[0]
		stored_pwd = row[2]
		if password == stored_pwd:
			return redirect(url_for('user_ui', id = userId))
		else:
			return render_template("main.html", title="Login Failed! Password Incorrect")
	else:
		#login doesn't exist
		return render_template("main.html", title="Login Failed! User Profile Does Not Exist!")
