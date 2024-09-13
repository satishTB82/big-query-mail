from azure.identity import DefaultAzureCredential
from azure.mgmt.apimanagement import ApiManagementClient
from azure.monitor.query import MetricsQueryClient
from azure.core.exceptions import HttpResponseError
from datetime import datetime, timedelta

def get_apim_details(subscription_id, resource_group_name, apim_name):
    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()
    
    # Create an ApiManagementClient instance
    apim_client = ApiManagementClient(credential, subscription_id)
    
    # List APIs in the API Management service
    apis = apim_client.api.list_by_service(resource_group_name, apim_name)
    
    # Extract API details
    api_details_list = []
    for api in apis:
        api_details_list.append({
            'SubscriptionID': subscription_id,
            'APIMName': apim_name,
            'APIID': api.id,
            'Name': api.name,
            'CallCountSuccess': 'N/A',  # Placeholder for metrics data
            'CallCountTotal': 'N/A'     # Placeholder for metrics data
        })
    
    return api_details_list

def get_api_metrics(subscription_id, resource_group_name, apim_name, api_id):
    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()
    
    # Create a MetricsQueryClient instance
    metrics_client = MetricsQueryClient(credential)
    
    # Define the time range for the metrics query (e.g., last 24 hours)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)
    
    # Define the API endpoint for metrics
    resource_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ApiManagement/service/{apim_name}/apis/{api_id}"
    
    # Query the metrics
    try:
        response = metrics_client.query_resource(
            resource_id=resource_id,
            metric_names=["TotalRequests", "SuccessfulRequests"],  # Use appropriate metrics
            timespan=f"{start_time.isoformat()}/{end_time.isoformat()}"
        )
        metrics = response.metrics

        # Extract call counts
        for metric in metrics:
            if metric.name == "TotalRequests":
                total_requests = metric.timeseries[0].data[-1].total
            if metric.name == "SuccessfulRequests":
                successful_requests = metric.timeseries[0].data[-1].total
        
        return {
            'CallCountSuccess': successful_requests,
            'CallCountTotal': total_requests
        }
    
    except HttpResponseError as e:
        print(f"Error fetching metrics: {e}")
        return {
            'CallCountSuccess': 'Error',
            'CallCountTotal': 'Error'
        }

# Replace with your subscription ID, resource group name, and APIM service name
subscription_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
resource_group_name = "your-resource-group"
apim_name = "your-apim-service"

# Get API details
api_details = get_apim_details(subscription_id, resource_group_name, apim_name)
print("API Details:")
for details in api_details:
    # Fetch metrics for each API
    metrics = get_api_metrics(subscription_id, resource_group_name, apim_name, details['APIID'])
    details.update(metrics)
    print(f"SubscriptionID: {details['SubscriptionID']}, APIMName: {details['APIMName']}, APIID: {details['APIID']}, Name: {details['Name']}, CallCountSuccess: {details['CallCountSuccess']}, CallCountTotal: {details['CallCountTotal']}")
