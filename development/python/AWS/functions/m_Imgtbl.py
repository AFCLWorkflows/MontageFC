import logging
import json
from MontagePy.main import mImgtbl
import boto3
import os
from subprocess import call

"""
This function exercutes mBackground to create the cimages.tbl table of
the corrected fits files located in <bucket-name>/corrected
return: - bucket-name
        - header
"""

def lambda_handler(event, context):
   
    s3_resource = boto3.resource('s3')
    s3 = boto3.client('s3')
    
    bucket_name = event['bucket']
    bucket = s3_resource.Bucket(bucket_name) 
    
    call('rm -rf /tmp/*', shell=True)
    os.mkdir('/tmp/images')
    
    for file in bucket.objects.filter(Prefix="corrected/"):
        file_name = file.key.split("corrected/")[1]
        s3.download_file(bucket_name, 'corrected/{}'.format(file_name), '/tmp/images/{}'.format(file_name))
  
    rtn = mImgtbl('/tmp/images', '/tmp/cimages.tbl')

    if rtn['status']=='1':
        return{
            'statusCode' : 400,
            'mImgtbl error: ' : rtn['msg']
        }

    try:
        response = s3.upload_file('/tmp/cimages.tbl', bucket_name, 'cimages.tbl')
    
    except Exception as e:
        logging.error(e)
    
    return{
        'statusCode': 200,
        'bucket' : bucket_name,
        'header' : event['header']
    }