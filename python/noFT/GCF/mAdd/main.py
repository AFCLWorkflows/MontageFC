
import logging
import json
from MontagePy.main import mAdd
import boto3
import botocore
import os


def main(request):   
   
    inputs = ["2mass-atlas-990502s-j1430092_corrected.fits","2mass-atlas-990502s-j1440198_corrected.fits", "2mass-atlas-990502s-j1420198_corrected.fits", "2mass-atlas-990502s-j1430080_corrected.fits", "2mass-atlas-990502s-j1420186_corrected.fits", "2mass-atlas-990502s-j1440186_corrected.fits"]

    
    #Replace with correct access keys for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxx") 


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
        

        return json.dumps({"output": "mosaic.fits"})  
        
    
    except Exception as e:
        logging.error(e)

        return json.dumps({"output": "Didn't work"})  
        
        
