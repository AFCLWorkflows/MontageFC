import logging
import json
import boto3
import os
from subprocess import call

"""
This function exercutes mBackground and uploads the corrected
fits file to <bucket-name>/corrected
return: - corrected file name
        - bucket-name
"""

def lambda_handler(event, context): 
    
    s3 = boto3.client('s3')
    call('rm -rf /tmp/*', shell=True)
    os.mkdir('/tmp/projected')
    
    file_name = event["filename"]
    bucket_name = event['bucket']
   
    projected ='projected/' + file_name
    projected_tmp = '/tmp/projected/' + file_name
   
    projected_area = projected[:len(projected) - 5] + '_area.fits'
    projected_area_tmp = '/tmp/projected/' + projected_area[10:]
    
    corrected_output = file_name[:len(projected) - 5] + "_corrected.fits"
    corrected_output_tmp = '/tmp/' + corrected_output
    
    pimages = 'pimages.tbl'
    pimages_tmp = '/tmp/' + pimages
    
    corrections = 'corrections.tbl'
    corrections_tmp = '/tmp/' + corrections

    try:
        s3.download_file(bucket_name, projected, projected_tmp)
        s3.download_file(bucket_name, projected_area, projected_area_tmp)
        s3.download_file(bucket_name, pimages, pimages_tmp)
        s3.download_file(bucket_name, corrections, corrections_tmp)
        
    except Exception as e:
        logging.error(e)
        
    status_file_tmp = '/tmp/statusfile.txt'
    rtn = call(["/opt/bin/mBackground", "-t", "-s", status_file_tmp, projected_tmp, corrected_output_tmp, pimages_tmp, corrections_tmp])

    if rtn == 1:
        file = open(status_file_tmp, "r")
        file_contents = file.read()
        file.close()
        return{
            'statusCode' : 400,
            'mBackground error: ' : file_contents
        }

    try:
        response = s3.upload_file(corrected_output_tmp, bucket_name, 'corrected/{}'.format(corrected_output))
    
    except Exception as e:
        logging.error(e)

    return{
        'statusCode': 200,
        'corrected': json.dumps(corrected_output),
        'bucket' : bucket_name
    }