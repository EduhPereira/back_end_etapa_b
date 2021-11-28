from flask import Blueprint
from app.routes.issue_blueprint import bp as bp_issue

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")

bp_api.register_blueprint(bp_issue)
