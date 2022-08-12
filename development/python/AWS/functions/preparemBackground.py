import json
import boto3

"""
This function is required for the following parallel function mBackground 
to get the projected file names
return: - list of file names which are located in <bucket-name>/projected
        - number of files
        - bucket-name
        - header
"""

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    bucket_name = event['bucket']
    bucket = s3.Bucket(bucket_name)
    
    filenames = []

    for file in bucket.objects.filter(Prefix="projected/"):
        file_name = file.key.split("projected/")[1]
        if file_name[-10:] != '_area.fits':
            filenames.append(file_name)
    
    return {
        'statusCode': 200,
        'filenames': filenames,
        'number' : len(filenames),
        'bucket' : bucket_name,
        'header' : event['header']
    }