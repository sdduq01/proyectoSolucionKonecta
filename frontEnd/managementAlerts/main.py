import functions_framework
from google.cloud import bigquery
from flask import jsonify, Request, make_response
import json
import time

client = bigquery.Client(location="EU")

PROJECT_ID = "kam-bi-451418"
DATASET = "QuickAlert"
TABLE = "SavedAlerts"
TABLE_ID = f"{PROJECT_ID}.{DATASET}.{TABLE}"

def cors_enabled_response(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

def is_data_in_streaming_buffer():
    try:
        query = f"""
            SELECT COUNT(*) AS count
            FROM `{TABLE_ID}`
            WHERE _PARTITIONTIME IS NULL
        """
        query_job = client.query(query)
        results = query_job.result()
        for row in results:
            return row.count > 0
    except Exception as e:
        print(f"Error al verificar el streaming buffer: {e}")
        return False

@functions_framework.http
def management_alerts(request: Request):
    try:
        # Manejo CORS preflight
        if request.method == 'OPTIONS':
            response = make_response('', 204)
            return cors_enabled_response(response)

        # Manejo GET
        if request.method == 'GET':
            action = request.args.get('action')
            if action == 'list':
                try:
                    query = f"SELECT * FROM `{TABLE_ID}`"
                    query_job = client.query(query)
                    results = [dict(row.items()) for row in query_job]
                    response = jsonify({'alerts': results})
                    return cors_enabled_response(response)
                except Exception as e:
                    return cors_enabled_response(jsonify({'error': f'Error al listar alertas: {str(e)}'})), 500
            else:
                return cors_enabled_response(jsonify({'error': 'Acción no válida en GET'})), 400

        # Manejo POST
        elif request.method == 'POST':
            try:
                request_json = request.get_json()
                if not request_json:
                    return cors_enabled_response(jsonify({'error': 'No se proporcionaron datos JSON válidos'})), 400

                action = request_json.get('action')
                alert_id = request_json.get('id')

                if not alert_id:
                    return cors_enabled_response(jsonify({'error': 'Falta el ID de la alerta'})), 400

                if action == 'delete':
                    if is_data_in_streaming_buffer():
                        print("Esperando 60 segundos por datos en el streaming buffer...")
                        time.sleep(60)

                    query = f"DELETE FROM `{TABLE_ID}` WHERE id = @id"
                    job_config = bigquery.QueryJobConfig(
                        query_parameters=[
                            bigquery.ScalarQueryParameter("id", "STRING", alert_id)
                        ]
                    )
                    client.query(query, job_config=job_config).result()
                    return cors_enabled_response(jsonify({'message': 'Alerta eliminada con éxito'}))

                elif action == 'toggle':
                    update_fields = {
                        'campaign': request_json.get('campaign'),
                        'metric': request_json.get('metric'),
                        'target': request_json.get('target'),
                        'frequency': request_json.get('frequency'),
                        'whatsapp': request_json.get('whatsapp'),
                        'email': request_json.get('email'),
                        'enabled': request_json.get('enabled')
                    }

                    if any(value is None for value in update_fields.values()):
                        return cors_enabled_response(jsonify({'error': 'Faltan campos para actualizar la alerta'})), 400

                    if is_data_in_streaming_buffer():
                        print("Esperando 60 segundos por datos en el streaming buffer...")
                        time.sleep(60)

                    query = f"""
                        UPDATE `{TABLE_ID}`
                        SET
                            campaign = @campaign,
                            metric = @metric,
                            target = @target,
                            frequency = @frequency,
                            whatsapp = @whatsapp,
                            email = @email,
                            enabled = @enabled
                        WHERE id = @id
                    """
                    job_config = bigquery.QueryJobConfig(
                        query_parameters=[
                            bigquery.ScalarQueryParameter("campaign", "STRING", update_fields['campaign']),
                            bigquery.ScalarQueryParameter("metric", "STRING", update_fields['metric']),
                            bigquery.ScalarQueryParameter("target", "STRING", update_fields['target']),
                            bigquery.ScalarQueryParameter("frequency", "STRING", update_fields['frequency']),
                            bigquery.ScalarQueryParameter("whatsapp", "STRING", update_fields['whatsapp']),
                            bigquery.ScalarQueryParameter("email", "STRING", update_fields['email']),
                            bigquery.ScalarQueryParameter("enabled", "BOOL", update_fields['enabled']),
                            bigquery.ScalarQueryParameter("id", "STRING", alert_id)
                        ]
                    )
                    client.query(query, job_config=job_config).result()
                    return cors_enabled_response(jsonify({'message': 'Alerta actualizada con éxito'}))

                else:
                    return cors_enabled_response(jsonify({'error': 'Acción no válida'})), 400

            except Exception as e:
                print(f"Error en el manejo POST: {e}")
                return cors_enabled_response(jsonify({'error': f'Error interno del servidor: {str(e)}'})), 500

        else:
            return cors_enabled_response(jsonify({'error': 'Método no permitido'})), 405

    except Exception as e:
        print(f"Error general: {e}")
        return cors_enabled_response(jsonify({'error': f'Error interno general: {str(e)}'})), 500
