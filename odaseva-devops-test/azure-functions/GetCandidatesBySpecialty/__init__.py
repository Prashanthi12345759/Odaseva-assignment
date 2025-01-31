import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient

app = func.FunctionApp()

@app.route(route="GetCandidatesBySpecialty/{specialty}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_candidates_by_specialty(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cosmos_endpoint = os.getenv('COSMOSDB_ENDPOINT')
    cosmos_key = os.getenv('COSMOSDB_KEY')

    cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
    database = cosmos_client.get_database_client('candidates')
    container = database.get_container_client('candidates')

    specialty = req.route_params.get('specialty')
    query = f"SELECT * FROM c WHERE c.specialty = '{specialty}'"
    items = list(container.query_items(query, enable_cross_partition_query=True))

    return func.HttpResponse(
        status_code=200,
        body=str(items)
    )