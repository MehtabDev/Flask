import json
from flask import Response
from bson import json_util


def return_response(error, error_message, status_code, data=None):
    if data is None:
        data = list()
    return_msg = json.dumps({"error": error, "message": error_message, "data": data}, default=json_util.default)
    response_data = Response(return_msg, status=status_code, mimetype='application/json')
    # resp.headers['Access-Control-Allow-Origin'] = '*' # can be uncomment if required
    return response_data