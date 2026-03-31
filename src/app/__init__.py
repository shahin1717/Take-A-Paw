# src/app/__init__.py
import os
from flask import Flask
from dotenv import load_dotenv

#start of flask app factory
def create_app(test_config=None):
    load_dotenv()

    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    
    print(f"📁 Template directory: {template_dir}")
    print(f"📁 Static directory: {static_dir}")
    
    if not os.path.exists(template_dir):
        print(f"❌ Template directory not found: {template_dir}")
        os.makedirs(template_dir, exist_ok=True)
        print("✅ Created templates directory")

    flask_app = Flask(__name__, 
                     template_folder=template_dir,
                     static_folder=static_dir)

    # secret key
    if not getattr(flask_app, "secret_key", None):
        flask_app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

    # DB - pass test_config if provided
    from .db import init_db
    init_db(flask_app, test_config)
    import cloudinary
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )
    # blueprints
    from .routes.auth import bp as auth_bp
    from .routes.pets import bp as pets_bp
    from .routes.admin import bp as admin_bp
    from .routes.quiz import bp as quiz_bp
    from .routes.system import bp as system_bp
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(pets_bp)
    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(quiz_bp)
    flask_app.register_blueprint(system_bp)

    print("🔗 Registered routes:")
    for r in flask_app.url_map.iter_rules():
        print(" ", r)

    return flask_app