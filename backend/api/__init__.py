# backend/api/__init__.py

import azure.functions as func
from server import main_handler  # your FastAPI/Flask-like logic

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return main_handler(req)
