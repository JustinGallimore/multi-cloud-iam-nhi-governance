import json
import csv

with open('aws_iam_audit.json', 'r') as f:
    aws_data = json.load(f)

with open('azure_iam_audit.json', 'r') as f:
    azure_data = json.load(f)

    rows = []

for user in aws_data['Users']:
    risk = 'None'
    for key in user['AccessKeys']:
        if key['NeedsRotation']:
            risk = 'Key needs rotation'
    rows.append({
        'Cloud': 'AWS',
        'IdentityType': 'IAM User',
        'Name': user['UserName'],
        'CreatedDate': user['UserCreateDate'],
        'Owner': '',
        'RiskFlag': risk
    })

for role in aws_data['Roles']:
    rows.append({
        'Cloud': 'AWS',
        'IdentityType': 'IAM Role',
        'Name': role['RoleName'],
        'CreatedDate': role['RoleCreateDate'],
        'Owner': '',
        'RiskFlag': 'Review trust policy'
    })

owned_app_ids = {app['AppId'] for app in azure_data['AppRegistrations']}

for sp in azure_data['ServicePrincipals']:
    is_owned = sp['AppId'] in owned_app_ids
    rows.append({
        'Cloud': 'Azure',
        'IdentityType': 'Service Principal',
        'Name': sp['DisplayName'],
        'CreatedDate': sp['CreatedDateTime'],
        'Owner': '' if is_owned else 'Microsoft / Third-Party (not tenant-owned)',
        'RiskFlag': 'Needs owner assignment' if is_owned else 'None - external service'
    })

for app in azure_data['AppRegistrations']:
    risk = 'None'
    for cred in app['PasswordCredentials']:
        if cred['Expired']:
            risk = 'Secret expired'
        elif risk == 'None':
            risk = 'Has active secret, verify rotation'
    rows.append({
        'Cloud': 'Azure',
        'IdentityType': 'App Registration',
        'Name': app['DisplayName'],
        'CreatedDate': app['CreatedDateTime'],
        'Owner': '',
        'RiskFlag': risk
  })      
for row in rows:
        if row['Owner'] == '':
            row['Owner'] = 'Justin Gallimore (Lab Owner)'

with open('docs/ownership_mapping.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Cloud', 'IdentityType', 'Name', 'CreatedDate', 'Owner', 'RiskFlag'])
        writer.writeheader()
        writer.writerows(rows)
print(f"Ownership mapping complete. {len(rows)} identities written to docs/ownership_mapping.csv")