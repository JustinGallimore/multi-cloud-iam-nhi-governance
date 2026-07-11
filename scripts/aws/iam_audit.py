import boto3
import json
from datetime import datetime, timezone

iam = boto3.client('iam')

def get_users():
    users = []
    paginator = iam.get_paginator('list_users')
    for page in paginator.paginate():
        for user in page['Users']:
            users.append(user)
    return users

def get_access_keys(username):
    keys = []
    response = iam.list_access_keys(UserName=username)
    for key in response['AccessKeyMetadata']:
        age_days = (datetime.now(timezone.utc) - key['CreateDate']).days
        keys.append({
            'AccessKeyId': key['AccessKeyId'],
            'Status': key['Status'],
            'CreateDate': str(key['CreateDate']),
            'AgeInDays': age_days
        })
    return keys

def get_roles():
    roles = []
    paginator = iam.get_paginator('list_roles')
    for page in paginator.paginate():
        for role in page['Roles']:
            roles.append({
                'RoleName': role['RoleName'],
                'RoleCreateDate': str(role['CreateDate']),
                'TrustPolicy': role['AssumeRolePolicyDocument']
            })
    return roles

def run_audit():
    audit_results = []
    users = get_users()
    roles = get_roles()  

    for user in users:
        username = user['UserName']
        keys = get_access_keys(username)

        for key in keys:
            key['NeedsRotation'] = key['AgeInDays'] > 90

        audit_results.append({
            'UserName': username,
            'UserCreateDate': str(user['CreateDate']),
            'AccessKeys': keys
        })

    output = {
        'Users': audit_results,
        'Roles': roles
    }

    with open('aws_iam_audit.json', 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    run_audit()