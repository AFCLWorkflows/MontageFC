import json
import os
import boto3
import logging
from subprocess import call

"""
This function is required to combine all diffs into fits.tbl which is needed
by mBgModel. Uploads fits.tbl to <bucket-name>
return: - bucket-name
        - header
"""

def lambda_handler(event, context):

    call('rm -rf /tmp/*', shell=True)
    os.mkdir('/tmp/diffs')

    s3= boto3.client('s3')
    bucket_name = event['bucket']
    
    try:
        s3.download_file(bucket_name, 'pimages.tbl', '/tmp/pimages.tbl')
        s3.download_file(bucket_name, 'diffs.tbl', '/tmp/diffs/diffs.tbl')
    
    except Exception as e:
        logging.error(e)

    rtn = call(["/opt/bin/mStatFile", "/tmp/diffs/"])
    
    if rtn != 0:
        return{
            'statusCode' : 400,
            'mFitplane error: ' : 'Invalid diffs.tbl'
        }
    
    response = s3.list_objects_v2(
        Bucket=bucket_name, Prefix='diffs/')
        
    s3_files = response["Contents"]
    for s3_file in s3_files:
        #Key: /diffs/file_name
        s3.download_file(bucket_name, s3_file["Key"], '/tmp/{}'.format(s3_file["Key"]))
    
    status_file_tmp = '/tmp/status_file.txt'
    rtn = call(["/opt/bin/mConcatFit", "-s", status_file_tmp, "/tmp/diffs/statfile.tbl", "/tmp/diffs/fits.tbl", "/tmp/diffs/"])
    
    if rtn == 1:
        file = open(status_file_tmp, "r")
        file_contents = file.read()
        file.close()
        return{
            'statusCode' : 400,
            'mConcatFit error: ' : file_contents
        }
    
    try:
        response = s3.upload_file('/tmp/diffs/fits.tbl', bucket_name, 'fits.tbl')
    
    except Exception as e:
        logging.error(e)

    return {
        'statusCode': 200,
        'bucket' : bucket_name,
        'header' : event['header']
    }
