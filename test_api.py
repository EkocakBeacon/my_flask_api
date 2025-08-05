import requests

# Change this to your deployed app URL
deployed_url = "https://beacon-sql-api.azurewebsites.net/"

# Test the home endpoint
resp = requests.get(deployed_url)
print(f"GET / response: {resp.status_code} - {resp.text}")

# Test the /run endpoint (replace 'your_table_name' with a real table)
run_url = deployed_url.rstrip('/') + '/run'
payload = {"query": "SELECT TOP 1 * FROM your_table_name"}
try:
    resp = requests.post(run_url, json=payload)
    print(f"POST /run response: {resp.status_code} - {resp.text}")
except Exception as e:
    print(f"Error posting to /run: {e}")
