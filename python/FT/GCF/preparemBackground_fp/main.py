

import json 

def prepare(request):

    request_json=request.get_json()

    failure_prob=request_json['failure_prob']

    return_list=[0,1,2,3,4,5]
    
    return json.dumps({"background_indices": return_list, "failure_prob":failure_prob})
    