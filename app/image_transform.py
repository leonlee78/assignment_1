from flask import render_template, redirect, url_for, request, abort
from app import webapp
from app.database import Database
import boto3

s3 = boto3.resource('s3')

@webapp.route('/image_transform',methods=['GET'])
#display user ui page
def s3_list():
	buckets = s3.buckets.all()
	return render_template("image_transform/list.html",title="Buckets",buckets=buckets)

@webapp.route('/image_transform/<id>',methods=['GET'])
#Display details about a specific bucket.
def s3_view(id):
	bucket = s3.Bucket(id)
	keys = bucket.objects.all()
	return render_template("image_transform/view.html",title="S3 Bucket Contents",id=id,keys=keys)

@webapp.route('/image_transform/upload/<id>', methods=['POST'])
#Upload a new file to an existing bucket
def s3_upload(id):
	database = Database()
	userid = 1
	f = request.files['new_file']
	if f.filename == '':
		abort(404)
	s3.Object(id,f.filename).put(Body=f)
	cnx = database.get_db()
	cursor = cnx.cursor()
	query = ''' INSERT INTO images (userId,key1) values (%s, %s)'''
	#TODO: get the userid
	print("Filename "+f.filename)
	cursor.execute(query, (userid, f.filename))
	return redirect(url_for('s3_view', id=id))