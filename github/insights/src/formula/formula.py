#!/usr/bin/python3
import os
import json


def Run(insightType, contribution):
    input_json = json.dumps({'contribution': contribution})

    if insightType == "ZupIT - Beagle":
        stdin_cmd = f"echo '{input_json}' | rit github get beagle-insights --stdin"

    elif insightType == "ZupIT - Charles":
        stdin_cmd = f"echo '{input_json}' | rit github get charles-insights --stdin"

    elif insightType == "ZupIT - Horusec":
        stdin_cmd = f"echo '{input_json}' | rit github get horusec-insights --stdin"

    elif insightType == "ZupIT - Ritchie":
        stdin_cmd = f"echo '{input_json}' | rit github get ritchie-insights --stdin"

    else:
        stdin_cmd = f"echo '{input_json}' | rit github get own-insights --stdin"

    os.system(f'{stdin_cmd}')