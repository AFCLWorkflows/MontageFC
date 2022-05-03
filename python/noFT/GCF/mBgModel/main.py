
import logging
import json
from MontagePy.main import mBgModel
import boto3
import botocore
import os


def main(request): 
   
  
    #Replace with correct access keys for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxx") 

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
    

    return json.dumps({"output": output})  
    
