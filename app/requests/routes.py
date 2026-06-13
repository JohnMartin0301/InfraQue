from flask import Blueprint

requests_bp = Blueprint('requests', __name__)

@requests_bp.route("/requests")
def requests_home():
    return "Requests page"