from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin-page")
def admin_home():
    print("ADMIN PAGE VISITED")
    return "Admin page"