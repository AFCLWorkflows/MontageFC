
import logging
import azure.functions as func
import json
from MontagePy.main import mAdd
import boto3
import botocore
import os
import random


def main(req: func.HttpRequest) -> func.HttpResponse:    
   
    inputs = ["2mass-atlas-990502s-j1430092_corrected.fits","2mass-atlas-990502s-j1440198_corrected.fits", "2mass-atlas-990502s-j1420198_corrected.fits", "2mass-atlas-990502s-j1430080_corrected.fits", "2mass-atlas-990502s-j1420186_corrected.fits", "2mass-atlas-990502s-j1440186_corrected.fits"]

    request_json = req.get_json()
    
    #Replace with keys valid for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") 

    failure_prob = request_json.get('failure_prob')
    
    if random.random() < (failure_prob/100):
        raise Exception('failure')


    try:
        os.mkdir('/tmp/images')

    except OSError as err:
        print(err)
            
    s3.download_file('montage-bucket', 'input/region.hdr', '/tmp/region.hdr')
    s3.download_file('montage-bucket', 'cimages.tbl', '/tmp/cimages.tbl')





    for input in inputs:
        input_path = 'corrected/' + input
        tmp_path= '/tmp/images/' + input
        s3.download_file('montage-bucket', input_path, tmp_path)


    try: 
        ret = mAdd('/tmp/images', '/tmp/cimages.tbl', '/tmp/region.hdr', '/tmp/mosaic.fits' )
    
        try:
            response = s3.upload_file('/tmp/mosaic.fits', 'montage-bucket', 'mosaic.fits')
        
        except ClientError as e:
            logging.error(e)
        

        return func.HttpResponse( 
            json.dumps({"output": "mosaic.fits", "failure_prob": failure_prob})  
        )
    
    except Exception as e:
        logging.error(e)

        return func.HttpResponse( 
            json.dumps({"output": "Didn't work", "failure_prob": failure_prob})  
        )
        
