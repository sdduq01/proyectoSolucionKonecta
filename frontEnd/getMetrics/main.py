from flask import jsonify, request
from google.cloud import bigquery

def get_metrics(request):
    if request.method == 'OPTIONS':
        # Respuesta a preflight
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json(silent=True)
    campaign = request_json.get("campaign") if request_json else None

    client = bigquery.Client()
    query = f"""
        SELECT DISTINCT Metrica
        FROM `kam-bi-451418.QuickAlert.LoadKpis`
        WHERE Campana = @campaign
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("campaign", "STRING", campaign)
        ]
    )

    results = client.query(query, job_config=job_config).result()
    metrics = [row["Metrica"] for row in results]

    return (jsonify(metrics), 200, headers)
