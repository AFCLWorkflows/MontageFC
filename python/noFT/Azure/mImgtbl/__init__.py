
import logging
import azure.functions as func
import json
from MontagePy.main import mImgtbl
import boto3
import botocore
import os


def main(req: func.HttpRequest) -> func.HttpResponse:    
   
    inputs = ["2mass-atlas-990502s-j1430092_corrected.fits","2mass-atlas-990502s-j1440198_corrected.fits", "2mass-atlas-990502s-j1420198_corrected.fits", "2mass-atlas-990502s-j1430080_corrected.fits", "2mass-atlas-990502s-j1420186_corrected.fits", "2mass-atlas-990502s-j1440186_corrected.fits"]

  

    #Replace with valid keys for bucket    
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") 




    for input in inputs:
        s3.download_file('montage-bucket', 'corrected/{}'.format(input), '/tmp/{}'.format(input))


  
    ret = mImgtbl('/tmp/', '/tmp/cimages.tbl')
    


    try:
        response = s3.upload_file('/tmp/cimages.tbl', 'montage-bucket', 'cimages.tbl')
    
    except ClientError as e:
        logging.error(e)
    

    return func.HttpResponse( 
        json.dumps({"output": 'cimages.tbl'})  
    )
