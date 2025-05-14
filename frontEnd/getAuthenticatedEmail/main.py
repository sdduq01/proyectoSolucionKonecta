# main.py

from flask import jsonify, make_response

def get_authenticated_email(request):
    if request.method == "OPTIONS":
        response = make_response('', 204)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    user_email = request.headers.get("X-Goog-Authenticated-User-Email", "anonimo@ninguno.com")

    response = jsonify({"email": user_email})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
