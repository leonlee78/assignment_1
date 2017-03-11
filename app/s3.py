import boto3
from datetime import datetime, timedelta
from operator import itemgetter
import botocore
s3 = boto3.resource('s3')
bucket = s3.Bucket('ece1779a')

class s3:
	def s3_delete(self):
		s3 = self.s3
		exists = True
		try:
		    s3.meta.client.head_bucket(Bucket='ece1779a')
		    for key in bucket.objects.all():
		    	key.delete()
		    #bucket.delete()
		    self.delete_images_database(userid)
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

	if __name__== "__main__":
		self.s3_delete()
