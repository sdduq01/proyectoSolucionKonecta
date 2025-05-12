import functions_framework
from google.cloud import bigquery
from flask import jsonify, make_response

client = bigquery.Client()

DATASET_ID = "QuickAlert"
TABLE_ID = "LoadKpis"

@functions_framework.http
def get_campaigns(request):
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    if request.method == 'OPTIONS':
        return make_response('', 204, cors_headers)

    if request.method != 'GET':
        return make_response('Method not allowed', 405, cors_headers)

    try:
        query = f"""
            SELECT DISTINCT Campana 
            FROM `kam-bi-451418.QuickAlert.LoadKpis`
            WHERE Campana IS NOT NULL
        """
        query_job = client.query(query)
        results = query_job.result()

        campaigns = [row['Campana'] for row in results]

        response = jsonify(campaigns)
        response.headers.update(cors_headers)
        return response

    except Exception as e:
        return make_response(f"Internal server error: {str(e)}", 500, cors_headers)