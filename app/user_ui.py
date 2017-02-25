from flask import render_template, redirect, url_for, request, g
from app import webapp

@webapp.route('/user_ui',methods=['GET'])
#display user ui page
def user_ui():
	return render_template("main.html",title="Login Page")
