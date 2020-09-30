#!/usr/bin/python3
import os
import json


def Run(insightType, contribution):
    input_json = json.dumps({'contribution': contribution})    
    
    if insightType == "ZupIT - CharlesCD":
        stdin_cmd = f"echo '{input_json}' | rit github get charles-insights --stdin"

    elif insightType == "ZupIT - Beagle":
        stdin_cmd = f"echo '{input_json}' | rit github get beagle-insights --stdin"
    
    elif insightType == "ZupIT - Ritchie":
        stdin_cmd = f"echo '{input_json}' | rit github get ritchie-insights --stdin"
    
    else:
        stdin_cmd = f"echo '{input_json}' | rit github get my-insights --stdin"

    os.system(f'{stdin_cmd}')