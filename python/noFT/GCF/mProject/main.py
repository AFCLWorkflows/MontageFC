 
import logging
import json
from MontagePy.main import mProject
import boto3
import botocore
import os


def main(request):   
   
    request_json = request.get_json()

  
    #Replace with correct access keys for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxx") 

    #input: file name of the image that should be projected. Has to be located in montage-bucket/input
    input = request_json.get('input')
    size = len(input)

    #input: file name of the header determines how the image should be projected. Has to be located in montage-bucket/input
    header = 'region.hdr'

    #output: generated file name that the projected image should have
    output = input
    size_output = len(output)
    output_area = output[:size_output - 5] + "_area.fits"

    input_path = 'input/' + input
    header_path = 'input/' + header

    input_tmp = '/tmp/' + input  
    header_tmp = '/tmp/' + header
    output_tmp = '/tmp/' + output
    output_area_tmp = '/tmp/' + output_area

    #logging.info(input, outupt, header)

    
    s3.download_file('montage-bucket', input_path, input_tmp)
    s3.download_file('montage-bucket', header_path, header_tmp)

  

    rtn = mProject(input_tmp, output_tmp, header_tmp)

    try:
        response = s3.upload_file(output_tmp, 'montage-bucket', 'projected/{}'.format(output))
        response = s3.upload_file(output_area_tmp, 'montage-bucket', 'projected/{}'.format(output_area))

    except ClientError as e:
        logging.error(e)
    

    return json.dumps({"output": output_area })  
    
