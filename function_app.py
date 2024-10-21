import azure.functions as func
import logging
import json
 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
 
# Dictionary to track all registered routes and methods
registered_routes = {
    "openapi": "3.0.1",
    "info": {
        "title": "Minimal API",
        "version": "1.0.0"
    },
    "paths": {}
}
 
def register_route(route: str, methods: list):
    """
    Registers a route and its corresponding methods in the global dictionary.
    """
    registered_routes["paths"][f"/{route}"] = {}
    
    for method in methods:
        registered_routes["paths"][f"/{route}"][method.lower()] = {
            "summary": f"{method} method for {route}",
            "responses": {
                "200": {
                    "description": f"Successful {method} request"
                }
            }
        }
@app.route(route="getitem", methods=["GET"])
def get_item(req: func.HttpRequest) -> func.HttpResponse:
    item_id = req.params.get('id')
    if item_id:
        return func.HttpResponse(f"GET request received. Item ID: {item_id}", status_code=200)
    else:
        return func.HttpResponse("ID not provided.", status_code=400)
 
register_route("getitem", ["GET"])
 
@app.route(route="createitem", methods=["POST"])
def create_item(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid request body.", status_code=400)
 
    item_name = req_body.get('name')
    if item_name:
        return func.HttpResponse(f"POST request received. Item name: {item_name}", status_code=201)
    else:
        return func.HttpResponse("Name not provided.", status_code=400)
 
register_route("createitem", ["POST"])
 
@app.route(route="updateitem", methods=["PUT"])
def update_item(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid request body.", status_code=400)
 
    item_id = req.params.get('id')
    item_name = req_body.get('name')
 
    if item_id and item_name:
        return func.HttpResponse(f"PUT request received. Item ID: {item_id}, New name: {item_name}", status_code=200)
    else:
        return func.HttpResponse("ID or Name not provided.", status_code=400)
 
register_route("updateitem", ["PUT"])
 
@app.route(route="deleteitem", methods=["DELETE"])
def delete_item(req: func.HttpRequest) -> func.HttpResponse:
    item_id = req.params.get('id')
    if item_id:
        return func.HttpResponse(f"DELETE request received. Item ID: {item_id}", status_code=200)
    else:
        return func.HttpResponse("ID not provided.", status_code=400)
 
register_route("deleteitem", ["DELETE"])
 
@app.route(route="getallitems", methods=["GET"])
def get_all_items(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("GET request received. List of items.", status_code=200)
 
register_route("getallitems", ["GET"])
 
@app.route(route="endpoints", methods=["GET"])
def list_endpoints(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("Fetching OpenAPI specification for all registered endpoints.")
        
        openapi_spec = registered_routes
        
        logging.info("OpenAPI specification fetched successfully.")
        
        return func.HttpResponse(
            body=json.dumps(openapi_spec, indent=2),
            status_code=200,
            mimetype="application/json"
        )
 
    except Exception as e:
        # Log the error with full traceback
        logging.error(f"Error fetching OpenAPI specification: {str(e)}", exc_info=True)
        return func.HttpResponse("Internal Server Error occurred while fetching OpenAPI spec.", status_code=500)
 
 
register_route("endpoints", ["GET"])
 
@app.route(route="newitem", methods=["GET"])
def newitem(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
 
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
 
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
register_route("newitem", ["GET"])
 
 
@app.route(route="listalldata", auth_level=func.AuthLevel.ANONYMOUS)
def listalldata(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
 
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
 
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
 
register_route("listalldata", ["GET"])
 