#!/usr/bin/python3
import json
import sys
import os
from datetime import datetime
import sys
import httpx

def run(doc_link):
    print("\033[1m\033[95m🔎 Getting Google Document insights...\033[0m")
    doc_id = ''.join([x for x in doc_link.split("?")[0].split("/") if len(x) == 44])
    if doc_id:
        print(f"\n\033[1m✅ Document ID:\033[0m {doc_id}\n")
    else:
        print(f"\n\033[91m❌ Document ID not found.\nPlease make sure you have something that looks like this in your link :\1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms\033[0m")
        exit()

    headers = {"X-Origin": "https://drive.google.com"}
    client = httpx.Client(headers=headers)

    url = f"https://clients6.google.com/drive/v2beta/files/{doc_id}?fields=alternateLink%2CcopyRequiresWriterPermission%2CcreatedDate%2Cdescription%2CdriveId%2CfileSize%2CiconLink%2Cid%2Clabels(starred%2C%20trashed)%2ClastViewedByMeDate%2CmodifiedDate%2Cshared%2CteamDriveId%2CuserPermission(id%2Cname%2CemailAddress%2Cdomain%2Crole%2CadditionalRoles%2CphotoLink%2Ctype%2CwithLink)%2Cpermissions(id%2Cname%2CemailAddress%2Cdomain%2Crole%2CadditionalRoles%2CphotoLink%2Ctype%2CwithLink)%2Cparents(id)%2Ccapabilities(canMoveItemWithinDrive%2CcanMoveItemOutOfDrive%2CcanMoveItemOutOfTeamDrive%2CcanAddChildren%2CcanEdit%2CcanDownload%2CcanComment%2CcanMoveChildrenWithinDrive%2CcanRename%2CcanRemoveChildren%2CcanMoveItemIntoTeamDrive)%2Ckind&supportsTeamDrives=true&enforceSingleParent=true&key=AIzaSyC1eQ1xj69IdTMeii5r7brs3R90eck-m7k"

    req = client.get(url)
    
    if "File not found" in str(req.text):
        print("\033[91m❌ This file does not exist or is not public\033[0m")
        exit()

    if "rateLimitExceeded" in req.text:
        for i in range(0,5):
            req = client.get(url)
            if "rateLimitExceeded" in req.text and i == 4:
                print("\033[91m❌ Rate Limit Exceeded. Try again later.\033[0m")
                exit()
            else:
                continue
    
    # Extracting informations          
    data = json.loads(req.text)
    
    # Dates
    created_date = datetime.strptime(data["createdDate"], '%Y-%m-%dT%H:%M:%S.%fz')
    modified_date = datetime.strptime(data["modifiedDate"], '%Y-%m-%dT%H:%M:%S.%fz')

    print(f"➡️  Creation date : {created_date.strftime('%Y/%m/%d %H:%M:%S')} (UTC)")
    print(f"➡️  Last edit date : {modified_date.strftime('%Y/%m/%d %H:%M:%S')} (UTC)")

    # Permissions
    user_permissions = []
    if data["userPermission"]:
        if data["userPermission"]["id"] == "me":
            user_permissions.append(data["userPermission"]["role"])
            if "additionalRoles" in data["userPermission"]:
                user_permissions += data["userPermission"]["additionalRoles"]

    public_permissions = []
    owner = None
    for permission in data["permissions"]:
        if permission["id"] in ["anyoneWithLink", "anyone"]:
            public_permissions.append(permission["role"])
            if "additionalRoles" in data["permissions"]:
                public_permissions += permission["additionalRoles"]
        elif permission["role"] == "owner":
            owner = permission

    print("\n\033[1m✅ Public permissions:\033[0m")
    for permission in public_permissions:
        print(f"- {permission}")

    if public_permissions != user_permissions:
        print("\033[1m⭐️ You have special permissions:\033[0m")
        for permission in user_permissions:
            print(f"- {permission}")

    if owner:
        print("\n\033[1m✅ Owner found!\033[0m")
        print(f"- Name : {owner['name']}")
        print(f"- Email : {owner['emailAddress']}")
        print(f"- Google ID : {owner['id']}")
