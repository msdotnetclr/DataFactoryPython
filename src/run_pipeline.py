from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
from datetime import datetime, timedelta
import time
from os import environ

"""
https://docs.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-python
https://docs.microsoft.com/en-us/python/api/overview/azure/data-factory?view=azure-python
"""


def print_activity_run_details(activity_run):
    """Print activity run details."""
    print("\n\tActivity run details\n")
    print("\tActivity run status: {}".format(activity_run.status))
    if activity_run.status == 'Succeeded':
        print("\tVariable name: {}".format(activity_run.output['name']))
        print("\tValue: {}".format(activity_run.output['value']))
    else:
        print("\tErrors: {}".format(activity_run.error['message']))


def main(tenant_id: str, subscription_id: str, client_id: str, client_secret: str):
    rg_name = "RG_Research"
    df_name = "DSTORM-ADF01"
    credentials = ClientSecretCredential(tenant_id, client_id, client_secret)

    adf_client = DataFactoryManagementClient(credentials, subscription_id)
    pipeline_name = 'pipeline1'
    run_response = adf_client.pipelines.create_run(rg_name, df_name, pipeline_name, parameters={'param1': 'test'})
    # Monitor the pipeline run
    time.sleep(30)
    pipeline_run = adf_client.pipeline_runs.get(
        rg_name, df_name, run_response.run_id)
    print("\n\tPipeline run status: {}".format(pipeline_run.status))
    filter_params = RunFilterParameters(
        last_updated_after=datetime.now() - timedelta(1), last_updated_before=datetime.now() + timedelta(1))
    query_response = adf_client.activity_runs.query_by_pipeline_run(
        rg_name, df_name, pipeline_run.run_id, filter_params)
    print_activity_run_details(query_response.value[0])


if __name__ == "__main__":
    main(environ.get('tenant_id'),
         environ.get('subscription_id'),
         environ.get('client_id'),
         environ.get('client_secret'))
