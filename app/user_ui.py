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

@webapp.route('/user_ui/<int:id>',methods=['GET'])
#display user ui page
def user_ui(id):
	#First check if the user has any pictures in the database
	cnx = get_db()
	
	cursor = cnx.cursor()
	
	query = ''' SELECT COUNT(1) FROM images WHERE usersId = %s '''
	
	cursor.execute(query, (id, ))
	
	row = cursor.fetchone()[0]
	
	userId = []
	
	userId.append(id)
	
	info_msg = "The current user has no images uploaded."
	
	if row:
		#Images exists
		return render_template("user_ui/view.html",title="Welcome!", userId = userId)
	else:
		#No Images
		return render_template("user_ui/view.html", title="Welcome!",userId = userId, info_msg = info_msg)

@webapp.route('/user_ui/upload/<int:id>', methods=['POST'])
#page for uploading an image and perform conversions
def upload_new_image(id):
	return 0
