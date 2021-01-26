#!/usr/bin/python3
import os
import json

def Run(insightType, contribution):
    input_json = json.dumps({'contribution': contribution})

    if insightType == "ZupIT - Beagle":
        stdin_cmd = f"echo '{input_json}' | rit github get beagle-insights --stdin"
        # input_flag_cmd = 'rit github get beagle-insights --contribution={}'.format(contribution)

    elif insightType == "ZupIT - Charles":
        stdin_cmd = f"echo '{input_json}' | rit github get charles-insights --stdin"
        # input_flag_cmd = 'rit github get charles-insights --contribution={}'.format(contribution)
        
    elif insightType == "ZupIT - Horusec":
        stdin_cmd = f"echo '{input_json}' | rit github get horusec-insights --stdin"
        # input_flag_cmd = 'rit github get horusec-insights --contribution={}'.format(contribution)
        
    elif insightType == "ZupIT - Ritchie":
        stdin_cmd = f"echo '{input_json}' | rit github get ritchie-insights --stdin"
        # input_flag_cmd = 'rit github get ritchie-insights --contribution={}'.format(contribution)
        
    else:
        stdin_cmd = f"echo '{input_json}' | rit github get own-insights --stdin"
        # input_flag_cmd = 'rit github get own-insights --contribution={}'.format(contribution)
        
    os.system(f'{stdin_cmd}')
    # os.system(f'{input_flag_cmd}')