import azure.functions as func
from azure.functions import WsgiMiddleware
from server import app  # your Flask app object

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return WsgiMiddleware(app).handle(req, context)
