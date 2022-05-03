
import logging
import json
from MontagePy.main import mBackground
import boto3
import botocore
import os
import random

def lambda_handler(event, context): 
   

    index = event['index']

    #Expected failure probability in percent
    failure_prob = event['failure_prob']

    #Introduce failure probability to function
    if random.random() < (failure_prob/100):
        raise Exception('failure')


    json_string = """{
    "0":{"input":"2mass-atlas-990502s-j1430092.fits", "a":"-1.93669e-03", "b":"-7.64968e-04", "c":"-1.14854e+00"},
    "1":{"input":"2mass-atlas-990502s-j1440198.fits", "a":"2.00328e-03 ", "b":"7.66052e-04", "c":"1.82079e-01"},
    "2":{"input":"2mass-atlas-990502s-j1420198.fits", "a":"-1.93669e-03 ", "b":"-7.64968e-04", "c":"-4.57375e-01"},
    "3":{"input":"2mass-atlas-990502s-j1430080.fits", "a":"0.00000e+00 ", "b":"0.00000e+00 ", "c":"0.00000e+00"},
    "4":{"input":"2mass-atlas-990502s-j1420186.fits", "a":"-2.77209e-02", "b":"-1.53323e-03 ", "c":"-5.82255e+00"},
    "5":{"input":"2mass-atlas-990502s-j1440186.fits", "a":"2.00328e-03", "b":"7.66049e-04", "c":"4.16277e-01"}
    }"""

    json_object = json.loads(json_string)


    background_input = json_object.get(str(index))


    input =  background_input.get('input')
    a = float(background_input.get('a'))
    b = float(background_input.get('b'))
    c = float(background_input.get('c'))



    input_path='projected/' + input

    input_path_size = len(input_path)
    input_area_path = input_path[:input_path_size - 5] + '_area.fits'

    input_tmp = '/tmp/' + input
    input_area_tmp = '/tmp/' + input_area_path[10:]

    
    size = len(input)
    output = input[:size - 5] + "_corrected.fits"
    output_tmp = '/tmp/' + output

    
  
    #Replace with correct AWS key for bucket
    s3 = boto3.client('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxxxx",  aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxx") 



    s3.download_file('montage-bucket', input_path, input_tmp)
    s3.download_file('montage-bucket', input_area_path, input_area_tmp)


  
    rtn = mBackground(input_tmp, output_tmp, a, b, c )


    try:
        response = s3.upload_file(output_tmp, 'montage-bucket', 'corrected/{}'.format(output))
    
    except ClientError as e:
        logging.error(e)
    

    return{
        'statusCode': 200,
        'body': json.dumps({"output": output, "failure_prob":failure_prob})  
    }
    
