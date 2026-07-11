import asyncio
import json
from datetime import datetime, timezone
from azure.identity import DefaultAzureCredential
from msgraph import GraphServiceClient

credential = DefaultAzureCredential()
scopes = ['https://graph.microsoft.com/.default']
graph_client = GraphServiceClient(credentials=credential, scopes=scopes)

async def get_service_principals():
    principals = []
    response = await graph_client.service_principals.get()

    while response is not None:
        for sp in response.value:
            principals.append({
                'DisplayName': sp.display_name,
                'AppId': sp.app_id,
                'ServicePrincipalId': sp.id,
                'ServicePrincipalType': sp.service_principal_type,
                'CreatedDateTime': str(sp.additional_data.get('createdDateTime')) if sp.additional_data else None
            })

        if response.odata_next_link:
            response = await graph_client.service_principals.with_url(response.odata_next_link).get()
        else:
            response = None

    return principals

async def get_app_registrations():
    apps = []
    response = await graph_client.applications.get()

    while response is not None:
        for app in response.value:
            secrets = []
            if app.password_credentials:
                for cred in app.password_credentials:
                    end_date = cred.end_date_time
                    age_days = None
                    expired = None
                    if end_date:
                        age_days = (datetime.now(timezone.utc) - end_date).days
                        expired = end_date < datetime.now(timezone.utc)
                    secrets.append({
                        'KeyId': str(cred.key_id),
                        'DisplayName': cred.display_name,
                        'EndDateTime': str(end_date),
                        'Expired': expired
                    })

            apps.append({
                'DisplayName': app.display_name,
                'AppId': app.app_id,
                'CreatedDateTime': str(app.created_date_time),
                'PasswordCredentials': secrets,
                'HasCertificates': bool(app.key_credentials)
            })

        if response.odata_next_link:
            response = await graph_client.applications.with_url(response.odata_next_link).get()
        else:
            response = None

    return apps

async def run_audit():
    principals = await get_service_principals()
    apps = await get_app_registrations()

    output = {
        'ServicePrincipals': principals,
        'AppRegistrations': apps
    }

    with open('azure_iam_audit.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Audit complete. {len(principals)} service principals scanned.")
    print(f"{len(apps)} app registrations scanned.")
    print("Results saved to azure_iam_audit.json")

if __name__ == '__main__':
    asyncio.run(run_audit())