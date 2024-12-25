from flask import Flask, render_template
from src.routes.web import web
from src.routes.api import api
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from src.utils.logger import setup_logging

app = Flask(__name__)
app.config.from_object('config.settings')
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)
)

# Register blueprints
app.register_blueprint(web)
app.register_blueprint(api, url_prefix='/api')

csrf = CSRFProtect()
csrf.init_app(app)

# Initialize logging
setup_logging()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
    return response

if __name__ == '__main__':
    app.run(debug=True) 