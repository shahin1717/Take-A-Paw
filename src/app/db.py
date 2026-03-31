# src/app/db.py
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app, test_config=None):
    # Use test database if provided
    if test_config and "SQLALCHEMY_DATABASE_URI" in test_config:
        app.config["SQLALCHEMY_DATABASE_URI"] = test_config["SQLALCHEMY_DATABASE_URI"]
        print("Using test database configuration")
    else:
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise RuntimeError("❌ DATABASE_URL is not set in .env")


        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    if "sqlalchemy" not in app.extensions:
        db.init_app(app)

    return db
