import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta

app = func.FunctionApp()

@app.route(route="GetCandidate/{candidateId}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_candidate(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cosmos_endpoint = os.getenv('COSMOSDB_ENDPOINT')
    cosmos_key = os.getenv('COSMOSDB_KEY')
    storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
    database = cosmos_client.get_database_client('candidates')
    container = database.get_container_client('candidates')

    candidate_id = req.route_params.get('candidateId')
    query = f"SELECT * FROM c WHERE c.candidateId = '{candidate_id}'"
    items = list(container.query_items(query, enable_cross_partition_query=True))

    if not items:
        return func.HttpResponse(
            status_code=404,
            body="Candidate not found."
        )

    candidate = items[0]
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container='resumes', blob=candidate['cvS3Key'])
    sas_url = blob_client.generate_blob_sas(
        permissions='r',
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    candidate['cvUrl'] = f"{blob_client.url}?{sas_url}"

    return func.HttpResponse(
        status_code=200,
        body=str(candidate)
    )