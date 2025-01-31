import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import base64

app = func.FunctionApp()

@app.route(route="CreateCandidate", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def create_candidate(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cosmos_endpoint = os.getenv('COSMOSDB_ENDPOINT')
    cosmos_key = os.getenv('COSMOSDB_KEY')
    storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
    database = cosmos_client.get_database_client('candidates')
    container = database.get_container_client('candidates')

    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_client = blob_service_client.get_container_client('resumes')

    req_body = req.get_json()
    specialty = req_body.get('specialty')
    candidate_id = req_body.get('candidateId')
    candidate_first_name = req_body.get('candidateFirstName')
    candidate_last_name = req_body.get('candidateLastName')
    candidate_birth_date = req_body.get('candidateBirthDate')
    cv = req_body.get('cv')

    cv_bytes = base64.b64decode(cv)
    blob_name = f"{specialty}/{candidate_id}.pdf"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(cv_bytes)

    candidate_item = {
        'specialty': specialty,
        'candidateId': candidate_id,
        'candidateFirstName': candidate_first_name,
        'candidateLastName': candidate_last_name,
        'candidateBirthDate': candidate_birth_date,
        'cvS3Key': blob_name
    }

    container.create_item(candidate_item)

    return func.HttpResponse(
        status_code=201,
        body=f"Candidate {candidate_id} created successfully."
    )