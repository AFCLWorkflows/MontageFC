import logging
import json
from MontagePy.main import mViewer
import boto3
import botocore
import os
import random


def main(request):  

    request_json = request.get_json()
   
    #Expected failure probability in percent
    failure_prob = request_json['failure_prob']

    #introduce failure probability
    if random.random() < (failure_prob/100):
        raise Exception('failure')
    
    #Insert correct AWS access keys for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx") 


    s3.download_file('montage-bucket', 'mosaic.fits', '/tmp/mosaic.fits')



    try: 
        ret = mViewer("-ct 1 -gray /tmp/mosaic.fits -2s max gaussian-log -out /tmp/mosaic.png", "/tmp/mosaic.png", mode=2)
    
        try:
            response = s3.upload_file('/tmp/mosaic.png', 'montage-bucket', 'mosaic.png')
        
        except Exception as e:
            logging.error(e)
        

        return json.dumps({"output": "mosaic.png"})  
        
    
    except Exception as e:
        logging.error(e)

        return json.dumps({"output": "Didn't work"})  
        
        
