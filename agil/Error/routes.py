from flask import Blueprint, render_template

error = Blueprint('error', __name__)


@error.app_errorhandler(404)
def error_404(error):
    return render_template('./error/404.html'), 404