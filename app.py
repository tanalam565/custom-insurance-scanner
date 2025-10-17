from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from api.routes import api

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize configuration
    Config.init_app(app)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    # Main route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )