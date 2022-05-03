import logging
import json
from MontagePy.main import mViewer
import boto3
import botocore
import os
import random


def lambda_handler(event, context):

    #Expected failure probability in percent
    failure_prob = event['failure_prob']

    #introduce failure probability
    if random.random() < (failure_prob/100):
        raise Exception('failure')
    
    #Replace with correct AWS key for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxx") 


    s3.download_file('montage-bucket', 'mosaic.fits', '/tmp/mosaic.fits')



    try: 
        ret = mViewer("-ct 1 -gray /tmp/mosaic.fits -2s max gaussian-log -out /tmp/mosaic.png", "/tmp/mosaic.png", mode=2)
    
        try:
            response = s3.upload_file('/tmp/mosaic.png', 'montage-bucket', 'mosaic.png')
        
        except Exception as e:
            logging.error(e)
        

        return{
            'statusCode': 200,
            'body': json.dumps({"output": "mosaic.png"})  
        } 
        
    
    except Exception as e:
        logging.error(e)
        
        
        return{
            'statusCode': 200,
            'body':  json.dumps({"output": "Didn't work"})  
        } 


        
        
