import logging
import json
from MontagePy.main import mDiff, mFitplane
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

    index = request_json['index']

    json_string = """{
    "0":{"first_index" : 0, "second_index" : 3, "first" : "2mass-atlas-990502s-j1430092.fits", "second": "2mass-atlas-990502s-j1430080.fits"},
    "1":{"first_index": 0, "second_index" : 4, "first" :  "2mass-atlas-990502s-j1430092.fits", "second": "2mass-atlas-990502s-j1420186.fits"},
    "2":{"first_index": 0, "second_index" : 5, "first":  "2mass-atlas-990502s-j1430092.fits", "second": "2mass-atlas-990502s-j1440186.fits"},
    "3":{"first_index": 1, "second_index" : 3, "first":  "2mass-atlas-990502s-j1440198.fits", "second": "2mass-atlas-990502s-j1430080.fits"},
    "4":{"first_index": 1, "second_index": 5, "first":  "2mass-atlas-990502s-j1440198.fits", "second": "2mass-atlas-990502s-j1440186.fits"},
    "5":{"first_index": 2, "second_index": 3, "first":  "2mass-atlas-990502s-j1420198.fits", "second": "2mass-atlas-990502s-j1430080.fits"},
    "6":{"first_index": 2, "second_index": 4, "first": "2mass-atlas-990502s-j1420198.fits",  "second": "2mass-atlas-990502s-j1420186.fits"},
    "7":{"first_index": 3, "second_index": 4, "first": "2mass-atlas-990502s-j1430080.fits", "second":  "2mass-atlas-990502s-j1420186.fits"},
    "8":{ "first_index": 3, "second_index": 5, "first": "2mass-atlas-990502s-j1430080.fits", "second":  "2mass-atlas-990502s-j1440186.fits"}
    }"""

    json_object = json.loads(json_string)

    diff_input = json_object.get(str(index))


    #Insert correct AWS access keys for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx") 

    first = diff_input.get('first')
    first_index = str(diff_input.get('first_index'))
   
    second = diff_input.get('second')
    second_index =str(diff_input.get('second_index'))

    header = 'region.hdr'


    output = 'diff.00000' + first_index + '.00000' + second_index + '.fits'

    first_path = 'projected/' + first
    first_path_size = len(first_path)
    first_area_path = first_path[:first_path_size - 5] + '_area.fits'

    second_path = 'projected/' + second
    second_path_size = len(second_path)
    second_area_path = second_path[:second_path_size - 5] + '_area.fits'

    header_path = 'input/' + header

    first_tmp = '/tmp/' + first 
    first_area_tmp = '/tmp/' + first_area_path[10:]
    second_tmp = '/tmp/' + second
    second_area_tmp = '/tmp/' + second_area_path[10:]

    header_tmp = '/tmp/' + header
    output_tmp = '/tmp/' + output
    
  

    s3.download_file('montage-bucket', first_path, first_tmp)
    s3.download_file('montage-bucket', second_path, second_tmp)
    s3.download_file('montage-bucket', first_area_path, first_area_tmp) 
    s3.download_file('montage-bucket', second_area_path, second_area_tmp) 
    s3.download_file('montage-bucket', header_path, header_tmp)

 

    try:
        rtn = mDiff(first_tmp, second_tmp, output_tmp, header_tmp)
        rtn_fit = mFitplane(output_tmp) 
        filename_fit = 'fit.00000' + first_index + '.00000' + second_index + '.txt'
        filename_tmp = '/tmp/'+ filename_fit
        file = open(filename_tmp, "w")
        file.write(str(rtn_fit))
        file.close()

        try:
            response = s3.upload_file(output_tmp, 'montage-bucket', 'diffs/{}'.format(output))
            response2 = s3.upload_file(filename_tmp, 'montage-bucket', 'diffs/{}'.format(filename_fit))
           
        except botocore.exceptions.ClientError as e:
            logging.error(e)
        

        return json.dumps({"output": filename_fit, "failure_prob":failure_prob})  
        

    except Exception as e: 
        logging.error(e)

        return json.dumps({"fit": "Images don't overlap. No fits file stored to diffs", "failure_prob":failure_prob})  
        
        


