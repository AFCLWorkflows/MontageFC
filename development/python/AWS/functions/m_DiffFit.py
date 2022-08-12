import logging
import json
import boto3
from subprocess import call
from MontagePy.main import mDiff, mFitplane

"""
This function executes first mDiff followed by mFitplane and uploads
output of mFitplane
return: - filename of mFitplane output
"""

def lambda_handler(event, context):
  
    s3= boto3.client('s3')
    bucket_name = event['bucket']
    header = event['header']
    diff_row = json.loads(event["diff"])

    first = str(diff_row["first"])
    first_index = str(diff_row["first_index"])
   
    second = str(diff_row["second"])
    second_index = str(diff_row["second_index"])

    first_path = 'projected/' + first
    first_area_path = first_path[:len(first_path) - 5] + '_area.fits'

    second_path = 'projected/' + second
    second_area_path = second_path[:len(second_path) - 5] + '_area.fits'

    header_tmp = '/tmp/' + header
    header_path = 'input/' + header

    first_tmp = '/tmp/' + first 
    first_area_tmp = '/tmp/' + first_area_path[10:]
    second_tmp = '/tmp/' + second
    second_area_tmp = '/tmp/' + second_area_path[10:]
    
    mDiff_output = 'diff.00000' + first_index + '.00000' + second_index + '.fits'
    mDiff_output_tmp = '/tmp/' + mDiff_output
    
    try:
        s3.download_file(bucket_name, first_path, first_tmp)
        s3.download_file(bucket_name, second_path, second_tmp)
        s3.download_file(bucket_name, first_area_path, first_area_tmp) 
        s3.download_file(bucket_name, second_area_path, second_area_tmp) 
        s3.download_file(bucket_name, header_path, header_tmp)
        
    except Exception as e:
        logging.error(e)
    
    rtn = mDiff(first_tmp, second_tmp, mDiff_output_tmp, header_tmp)

    filename_fit = 'fit.00000' + first_index + '.00000' + second_index + '.txt'
    filename_tmp = '/tmp/'+ filename_fit
        
    rtn_fit = call(["/opt/bin/mFitplane", "-s", filename_tmp, mDiff_output_tmp])
    
    if rtn_fit==1:
        file = open(filename_tmp, "r")
        file_contents = file.read()
        file.close()
        return{
            'statusCode' : 400,
            'mFitplane error: ' : file_contents
        }
        
    try:
        response = s3.upload_file(filename_tmp, bucket_name, 'diffs/{}'.format(filename_fit))
           
    except Exception as e:
        logging.error(e)
        
    return {
        'statusCode': 200,
        'fit.txt' : filename_fit
    }
