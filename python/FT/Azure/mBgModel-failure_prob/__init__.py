
import logging
import azure.functions as func
import json
from MontagePy.main import mBgModel
import boto3
import botocore
import os
import random


def main(req: func.HttpRequest) -> func.HttpResponse:    
   
  
    #Replace with keys valid for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") 

    request_json = req.get_json()
    failure_prob = request_json.get('failure_prob')
    
    if random.random() < (failure_prob/100):
        raise Exception('failure')

    
    filename_pimages = 'projected/pimages.tbl'
    filename_fits = 'diffs/fits.tbl'

    pimages_tmp = '/tmp/pimages.tbl'
    fits_tmp = '/tmp/fits.tbl'


    output = 'corrected.tbl'
    filename_output = '/tmp/corrected.tbl'



    s3.download_file('montage-bucket', filename_pimages, pimages_tmp)
    s3.download_file('montage-bucket', filename_fits, fits_tmp)

  

    rtn = mBgModel(pimages_tmp, fits_tmp, filename_output)

    try:
        response = s3.upload_file(filename_output, 'montage-bucket', '{}'.format(output))
    
    except ClientError as e:
        logging.error(e)
    

    return func.HttpResponse( 
        json.dumps({"output": output, "failure_prob": failure_prob})  
    )
