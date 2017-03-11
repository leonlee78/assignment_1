import boto3
from datetime import datetime, timedelta
from operator import itemgetter
import botocore

class S3:
	s3 = boto3.resource('s3')
	bucket = s3.Bucket('ece1779a')

	def get_bucket_list(self):
		buckets = self.s3.buckets.all()
		return buckets

	def get_bucket_keys(self,id):
		buck = self.s3.Bucket(id)
		print("****************")
		print(buck)
		keys = buck.objects.all()
		print(keys)
		return keys

	def upload_file(self,request):
		database = Database()
		s3 = self.s3
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

	def s3_delete(self):
		s3 = self.s3
		bucket = self.bucket
		exists = True
		try:
		    s3.meta.client.head_bucket(Bucket='ece1779a')
		    for key in bucket.objects.all():
		    	key.delete()
		    #bucket.delete()
		    #self.delete_images_database(userid)
		except botocore.exceptions.ClientError as e:
		    # If a client error is thrown, then check that it was a 404 error.
		    # If it was a 404 error, then the bucket does not exist.
		    error_code = int(e.response['Error']['Code'])
		    if error_code == 404:
		        exists = False

	def delete_images_database(self,userid):
		database = Database()
		cnx = database.get_db()
		cursor = cnx.cursor()
		query = 'DELETE FROM IMAGES WHERE ID = %s'
		cursor.execute(query, (userid))

'''
if __name__== "__main__":
	s3 = S3()
	s3.s3_delete()
'''
