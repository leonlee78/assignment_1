from flask import render_template, redirect, url_for, request, abort
from app import webapp
from app.database import Database
import boto3
from app.s3 import S3

s3 = S3()

@webapp.route('/image_transform',methods=['GET'])
#display user ui page
def s3_list():
	buckets = s3.get_bucket_list()
	return render_template("image_transform/list.html",title="Buckets",buckets=buckets)

@webapp.route('/image_transform/<id>',methods=['GET'])
#Display details about a specific bucket.
def s3_view(id):
	keys = s3.get_bucket_keys(id)
	print(keys)
	return render_template("image_transform/view.html",title="S3 Bucket Contents",id=id,keys=keys)

@webapp.route('/image_transform/upload/<id>', methods=['POST'])
#Upload a new file to an existing bucket
def s3_upload(id):
	s3.upload_file(request)
	return redirect(url_for('s3_view', id=id))