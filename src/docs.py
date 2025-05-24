from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
import os

docs_bp = Blueprint('docs', __name__)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "SyntPanel API"}
)

def register_docs(app):
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
