
import logging
import azure.functions as func
import json
from MontagePy.main import mViewer
import boto3
import botocore
import os
import random


def main(req: func.HttpRequest) -> func.HttpResponse:    

    request_json = req.get_json()
    failure_prob = request_json.get('failure_prob')
    
    if random.random() < (failure_prob/100):
        raise Exception('failure')

    
    #Replace with keys valid for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") 


    s3.download_file('montage-bucket', 'mosaic.fits', '/tmp/mosaic.fits')



    try: 
        ret = mViewer("-ct 1 -gray /tmp/mosaic.fits -2s max gaussian-log -out /tmp/mosaic.png", "/tmp/mosaic.png", mode=2)
    
        try:
            response = s3.upload_file('/tmp/mosaic.png', 'montage-bucket', 'mosaic.png')
        
        except Exception as e:
            logging.error(e)
        

        return func.HttpResponse( 
            json.dumps({"output": "mosaic.png"})  
        )
    
    except Exception as e:
        logging.error(e)

        return func.HttpResponse( 
            json.dumps({"output": "Didn't work"})  
        )
        
