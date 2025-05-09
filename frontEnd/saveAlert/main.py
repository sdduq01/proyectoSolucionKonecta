import functions_framework
from google.cloud import bigquery
import datetime
import json
import logging
from flask import Response

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Inicializar cliente de BigQuery
client = bigquery.Client()

# Definir dataset y tabla
DATASET_ID = "QuickAlert"
TABLE_ID = "SavedAlerts"

@functions_framework.http
def save_alert(request):
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    if request.method == 'OPTIONS':
        return Response('', status=204, headers=cors_headers)

    if request.method != 'POST':
        return Response('Method not allowed', status=405, headers=cors_headers)

    try:
        data = request.get_json()

        if not data:
            return Response("Bad request: Invalid JSON", status=400, headers=cors_headers)

        required_fields = ["campaign", "metric", "target"]
        for field in required_fields:
            if field not in data or not data[field]:
                return Response(f"Missing required field: {field}", status=400, headers=cors_headers)

        row = {
            "campaign": data.get("campaign"),
            "metric": data.get("metric"),
            "target": data.get("target"),
            "frequency": data.get("frequency"),
            "whatsapp": data.get("whatsapp"),
            "email": data.get("email"),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        logger.info("✅ Datos a insertar: %s", json.dumps(row, indent=2))

        table_ref = f"{client.project}.{DATASET_ID}.{TABLE_ID}"

        errors = client.insert_rows_json(table_ref, [row])

        if errors:
            logger.error("❌ Error al insertar datos en BigQuery: %s", errors)
            return Response("Error inserting data", status=500, headers=cors_headers)

        logger.info("✅ Datos insertados correctamente en BigQuery: %s", row)
        return Response("Alert saved successfully", status=200, headers=cors_headers)

    except Exception as e:
        logger.exception("❌ Excepción durante la ejecución de la función: %s", str(e))
        return Response(f"Internal server error: {str(e)}", status=500, headers=cors_headers)
