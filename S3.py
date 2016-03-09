import boto
import boto.s3.connection
access_key = 'jaysboto'
secret_key = 'secretkey'

conn = boto.connect_s3(
        aws_access_key_id = access_key, 
        aws_secret_access_key = secret_key,
        host = 'objects.dreamhost.com', 
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

## listing owned buckets
for bucket in conn.get_all_buckets():
       print "{name}\t{created}".format(
               name = bucket.name,
               created = bucket.creation_date,
       )
       
# < output >      
# mahbuckat1   2011-04-21T18:05:39.000Z
# mahbuckat2   2011-04-21T18:05:48.000Z
# mahbuckat3   2011-04-21T18:07:18.000Z

## Create a bucket 
bucket = conn.create_bucket('my-new-bucket')

## Listing a bucket's content
for key in bucket.list():
        print "{name}\t{size}\t{modified}".format(
                name = key.name, 
                size = key.size,
                modified = key.last_modified, 
                )

# < output >
# myphoto1.jpg 251262  2011-08-08T21:35:48.000Z
# myphoto2.jpg 262518  2011-08-08T21:38:01.000Z

## deleting a bucket 
conn.delete_bucket(bucket.name)

# creating an object
key = bucket.new_key('hello.txt')
key.set_contents_from_string('Hello World!')

# Change an object's ACL
hello_key = bucket.get_key('hello.txt')
hello_key.set_canned_acl('public-read')
plans_key = bucket.get_key('secret_plans.txt')
plans_key.set_canned_acl('private')

# download an object (to a file)
key = bucket.get_key('perl_poetry.pdf')
key.get_contents_to_filename('/home/jay/documents/perl_poetry.pdf')

# delete an object
bucket.delete_key('goodbye.txt')

# generate object download urls (signed and unsigned)
hello_key = bucket.get_key('hello.txt')
hello_url = hello_key.generate_url(0, query_auth=False, force_http=True)
print hello_url

plans_key = bucket.get_key('secret_plans.txt')
plans_url = plans_key.generate_url(3600, query_auth=True, force_http=True)
print plans_url

# <output> 
# http://objects.dreamhost.com/my-bucket-name/hello.txt
# http://objects.dreamhost.com/my-bucket-name/secret_plans.txt?Signature=XXXXXXXXXXXXXXXXXXXXXXXXXXX&Expires=1316027075&AWSAccessKeyId=XXXXXXXXXXXXXXXXXXX

