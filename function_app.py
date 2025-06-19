import azure.functions as func
import logging
import json
from datetime import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="hello")
def hello_world(req: func.HttpRequest) -> func.HttpResponse:
    """
    Simple HTTP trigger function that returns a greeting message.
    """
    logging.info('Python HTTP trigger function processed a request.')

    # Get name from query parameter or request body
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            if req_body:
                name = req_body.get('name')

    if name:
        message = f"Hello, {name}! This Azure Function was triggered at {datetime.utcnow().isoformat()}Z"
    else:
        message = f"Hello, World! This Azure Function was triggered at {datetime.utcnow().isoformat()}Z"

    return func.HttpResponse(
        json.dumps({
            "message": message,
            "status": "success",
            "timestamp": datetime.utcnow().isoformat()
        }),
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="data", methods=["GET", "POST"])
def process_data(req: func.HttpRequest) -> func.HttpResponse:
    """
    Function to process data - demonstrates both GET and POST methods.
    """
    logging.info('Data processing function triggered.')
    
    if req.method == "GET":
        # Return sample data for GET requests
        sample_data = {
            "items": [
                {"id": 1, "name": "Item 1", "value": 100000000000000000},
                {"id": 2, "name": "Item 2", "value": 20000000000000000000000000000},
                {"id": 3, "name": "Item 3", "value": 300}
            ],
            "total": 3,
            "timestamp": datetime.utcnow().isoformat()
        }
        return func.HttpResponse(
            json.dumps(sample_data),
            status_code=200,
            mimetype="application/json"
        )
    
    elif req.method == "POST":
        # Process posted data
        try:
            req_body = req.get_json()
            if req_body:
                # Simple data processing - double the values
                processed_data = {
                    "original": req_body,
                    "processed": {k: v * 2 if isinstance(v, (int, float)) else v 
                                for k, v in req_body.items()},
                    "timestamp": datetime.utcnow().isoformat()
                }
                return func.HttpResponse(
                    json.dumps(processed_data),
                    status_code=200,
                    mimetype="application/json"
                )
            else:
                return func.HttpResponse(
                    json.dumps({"error": "No JSON data provided"}),
                    status_code=400,
                    mimetype="application/json"
                )
        except Exception as e:
            logging.error(f"Error processing data: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON data"}),
                status_code=400,
                mimetype="application/json"
            )