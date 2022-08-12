import json
import boto3

"""
This function is required for the following parallel function mProjectPP 
to get the input file names
return: - list of file names which are located in <bucket-name>/input
        - number of files
        - bucket-name
"""

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    bucket_name = event['bucket']
    bucket = s3.Bucket(bucket_name)
    
    file_names = []

    #input files needs to be located at <bucket-name>/input
    for file in bucket.objects.filter(Prefix="input/"):
        file_name = file.key.split("input/")[1]
        if file_name[-4:] != '.hdr' and file_name != "" :
            file_names.append(file_name)
    
    return {
        'statusCode': 200,
        'filenames': file_names,
        'number' : len(file_names),
        'bucket' : bucket_name,
        'header' : event['header']
    }
