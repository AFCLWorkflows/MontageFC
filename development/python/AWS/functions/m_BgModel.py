import logging
import json
from MontagePy.main import mBgModel
import boto3
import os

"""
This function executes mBgModel and uploads corrections.tbl to <bucket-name
return: - bucket-name
        - header
"""

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    bucket_name = event['bucket']

    filename_pimages = 'pimages.tbl'
    filename_fits = 'fits.tbl'

    pimages_tmp = '/tmp/pimages.tbl'
    fits_tmp = '/tmp/fits.tbl'

    filename_corrections = 'corrections.tbl'
    corrections_tmp = '/tmp/corrections.tbl'

    try:
        s3.download_file(bucket_name, filename_pimages, pimages_tmp)
        s3.download_file(bucket_name, filename_fits, fits_tmp)
        
    except Exception as e:
        logging.error(e)

    rtn = mBgModel(pimages_tmp, fits_tmp, corrections_tmp)
    
    if rtn['status']=='1':
        return{
            'statusCode' : 400,
            'mBgModel error: ' : rtn['msg']
        }

    try:
        response = s3.upload_file(corrections_tmp, bucket_name, '{}'.format(filename_corrections))
    
    except Exception as e:
        logging.error(e)

    return {
        'statusCode': 200,
        'bucket' : bucket_name,
        'header' : event['header']
    }