import logging
import json
from MontagePy.main import mAdd
import boto3
import os
from subprocess import call

"""
This function executes mAdd and uploads the output file
mosaic.fits to <bucket-name>
return: - mosaic file name
        - bucket-name
"""

def lambda_handler(event, context):

    s3_resource = boto3.resource('s3')
    s3 = boto3.client('s3')
    
    header = event['header']
    bucket_name = event['bucket']
    bucket = s3_resource.Bucket(bucket_name)
    
    call('rm -rf /tmp/*', shell=True)
    os.mkdir('/tmp/images')

    try:
        for file in bucket.objects.filter(Prefix="corrected/"):
            file_name = file.key.split("corrected/")[1]
            s3.download_file(bucket_name, 'corrected/{}'.format(file_name), '/tmp/images/{}'.format(file_name))
            
        s3.download_file(bucket_name, 'input/' + header, '/tmp/' + header)
        s3.download_file(bucket_name, 'cimages.tbl', '/tmp/cimages.tbl')
    
    except Exception as e:
            logging.error(e)

    rtn = mAdd('/tmp/images', '/tmp/cimages.tbl', '/tmp/' + header, '/tmp/mosaic.fits' )
    
    if rtn['status']=='1':
        return{
            'statusCode' : 400,
            'mAdd error: ' : rtn['msg']
        }
    
    try:
        response = s3.upload_file('/tmp/mosaic.fits', bucket_name, 'mosaic.fits')
        
    except Exception as e:
        logging.error(e)

    return{
        'statusCode': 200,
        'mosaic name': "mosaic.fits",
        'bucket' : bucket_name
    }