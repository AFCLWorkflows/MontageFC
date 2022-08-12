import logging
import json
from MontagePy.main import mViewer
import boto3
import os

"""
This function executes mViewer to create the mosaic.png file and uploads
it to <bucket-name>
return: - bucket-name
"""


def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    bucket_name = event['bucket']
    
    try:
        s3.download_file(bucket_name, 'mosaic.fits', '/tmp/mosaic.fits')
    
    except Exception as e:
        logging.error(e)
    
    rtn = mViewer("-ct 1 -gray /tmp/mosaic.fits -2s max gaussian-log -out /tmp/mosaic.png", "/tmp/mosaic.png", mode=2)
    
    if rtn['status']=='1':
        return{
            'statusCode' : 400,
            'mViewer error: ' : rtn['msg']
        }
    
    try:
        response = s3.upload_file('/tmp/mosaic.png', bucket_name, 'mosaic.png')
        
    except Exception as e:
        logging.error(e)

    return{
        'statusCode': 200,
        'final picture': "mosaic.png"
    } 
        