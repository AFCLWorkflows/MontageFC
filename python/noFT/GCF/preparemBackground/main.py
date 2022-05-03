

import json 

def prepare(request):
    return_list=[0,1,2,3,4,5]
    
    return json.dumps({"background_indices": return_list})
    