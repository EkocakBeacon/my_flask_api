import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import Site, SiteConfig, SkuDescription

# Azure setup
subscription_id = '06455709-4296-4354-8bcc-6ded218b9f69'
resource_group = 'beacon-flask-rg'
location = 'swedencentral'
app_service_plan = 'beacon-flask-plan'
web_app_name = 'beacon-sql-api'
zip_path = 'C:/Users/Egehan/Desktop/flask_deploy.zip'

# Authenticate
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)
web_client = WebSiteManagementClient(credential, subscription_id)

# Step 1: Resource group
print("Creating resource group...")
resource_client.resource_groups.create_or_update(resource_group, {"location": location})

# Step 2: App Service plan
print("Creating App Service plan...")
web_client.app_service_plans.begin_create_or_update(
    resource_group,
    app_service_plan,
    {
        "location": location,
        "sku": SkuDescription(name="B1", tier="Basic", size="B1", capacity=1),
        "reserved": True,
    },
).result()

# Step 3: Web App
print("Creating Web App...")
site_config = SiteConfig(app_settings=[
    {"name": "WEBSITE_RUN_FROM_PACKAGE", "value": "1"},
])
web_client.web_apps.begin_create_or_update(
    resource_group,
    web_app_name,
    Site(
        location=location,
        server_farm_id=app_service_plan,
        site_config=site_config,
        kind="app,linux",
    )
).result()

# Step 4: Deploy ZIP using CLI
print("Deploying ZIP package...")
os.system(
    f'az webapp deploy --resource-group {resource_group} '
    f'--name {web_app_name} --src-path "{zip_path}" --type zip'
)

print(f"✅ Deployed successfully: https://{web_app_name}.azurewebsites.net")
