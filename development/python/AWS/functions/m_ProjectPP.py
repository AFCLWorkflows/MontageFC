import logging
import json
import boto3
from MontagePy.main import mProjectPP
from subprocess import call

"""
This function executes mProjectPP on the input file and uploads the projected
fits file and the _area fits file on <bucket-name>/projected
return: - projected file name
"""

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    bucket_name = event['bucket']

    input_file = event['filename']
    header = event['header']

    #projected_file: same name as the input file
    projected_file = input_file
    projected_file_area = projected_file[:len(projected_file) - 5] + "_area.fits"

    input_file_path = 'input/' + input_file
    header_path = 'input/' + header

    input_file_tmp = '/tmp/' + input_file
    header_tmp = '/tmp/' + header
    
    projected_file_tmp = '/tmp/' + projected_file
    projected_file_area_tmp = '/tmp/' + projected_file_area
    
    try:
        s3.download_file(bucket_name, input_file_path, input_file_tmp)
        s3.download_file(bucket_name, header_path, header_tmp)
        
    except Exception as e:
        logging.error(e)
    
    rtn = mProjectPP(input_file_tmp, projected_file_tmp, header_tmp)

    if rtn['status']=='1':
        return{
            'statusCode' : 400,
            'mProjectPP error: ' : rtn['msg']
        }

    try:
        response = s3.upload_file(projected_file_tmp, bucket_name, 'projected/{}'.format(projected_file))
        response = s3.upload_file(projected_file_area_tmp, bucket_name, 'projected/{}'.format(projected_file_area))

    except Exception as e:
        logging.error(e)

    return{
        'statusCode': 200,
        'projected' : projected_file
    }