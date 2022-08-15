import json
from storage.pyStorage import pyStorage


def lambda_handler(event, context):
    
    
    pyStorage.create_cred_file(
        aws_access_key_id = event['aws_access_key_id'],
        aws_secret_access_key = event['aws_secret_key'],
        aws_session_token = event['aws_session_token'],
        gcp_client_email = event['client_email'],
        gcp_private_key = event['private_key'],
        gcp_project_id = event['project_id']
        )
    
    source_url = event['source_url']
    targets = event['targets']
    
    response = []
    local_filename = '/tmp/' + source_url.split('/')[-1]
    pyStorage.copy(source_url, local_filename)
    
    for t in targets:
       x =  pyStorage.copy(local_filename, t)
       response.append(x)
    
    print(local_filename)
        
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }