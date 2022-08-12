import json
import logging
import boto3
from MontagePy.main import mShrink

"""
This function executes mShrink to shrink the mosaic.fits file and uploads
shrinked file to <bucket-name>
return: - bucket-name
"""

def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    bucket_name = event['bucket']
    
    shrink_value = 1.5
    
    try:
        s3.download_file(bucket_name, 'mosaic.fits', '/tmp/mosaic.fits')
    
    except Exception as e:
        logging.error(e)
    
    rtn = mShrink('/tmp/mosaic.fits', '/tmp/mosaic.fits', shrink_value)
    
    if rtn['status']=='1':
        return{
            'statusCode' : 400,
            'mShrink error: ' : rtn['msg']
        }
    
    try:
        response = s3.upload_file('/tmp/mosaic.fits', bucket_name, 'mosaic.fits')
        
    except Exception as e:
        logging.error(e)
            
    return {
        'statusCode': 200,
        'bucket' : bucket_name
    }
