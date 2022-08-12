import json
from MontagePy.main import mImgtbl, mOverlaps
import boto3
import logging
import os
import pandas
from subprocess import call

"""
This function is required for the following parallel function mDiffFit.
Generates a list of differences from diffs.tbl. Uploads pimages.tbl and diffs.tbl
return: - list of diff rows
        - number of files
        - bucket-name
        - header
"""

def lambda_handler(event, context):
    
    call('rm -rf /tmp/*', shell=True)
    os.mkdir('/tmp/projected')
    os.mkdir('/tmp/diffs')
    
    s3 = boto3.client("s3")
    bucket_name = event['bucket']
 
    response = s3.list_objects_v2(
        Bucket=bucket_name, Prefix='projected/')
        
    s3_files = response["Contents"]
    
    try:
        for s3_file in s3_files:
            #Key: /projected/file_name
            s3.download_file(bucket_name, s3_file["Key"], '/tmp/{}'.format(s3_file["Key"]))
        
    except Exception as e:
        logging.error(e)
    
    rtn = mImgtbl('/tmp/projected', '/tmp/pimages.tbl') 
    
    if rtn['status']=='1':
        return{
            'statusCode' : 400,
            'mImgtbl error: ' : rtn['msg']
        }
    
    rtn = mOverlaps("/tmp/pimages.tbl", "/tmp/diffs/diffs.tbl")
    
    if rtn['status']=='1':
        return{
            'statusCode' : 400,
            'mOverlaps error: ' : rtn['msg']
        }
    
    diff_table = pandas.read_table('/tmp/diffs/diffs.tbl', skiprows=2, delim_whitespace=True, header=None, index_col=None)
    diff_rows = []

    for row in diff_table.values:
        diff_row = json.dumps({
            "first_index": row[0],
            "second_index": row[1],
            "first": row[2],
            "second": row[3],
        })
        diff_rows.append(diff_row)
    
    try:
        response = s3.upload_file('/tmp/pimages.tbl', bucket_name, 'pimages.tbl')
        response = s3.upload_file('/tmp/diffs/diffs.tbl', bucket_name, 'diffs.tbl')
    
    except Exception as e:
        logging.error(e)
    
    return {
        'statusCode': 200,
        'diff_rows': diff_rows,
        'number': len(diff_table),
        'bucket' : bucket_name,
        'header' : event['header']
    }
