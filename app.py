import os
from flask import Flask, jsonify
from resources.shop import blueprint as ShopBluePrint
from resources.product import blueprint as ProductBluePrint
from resources.user import blueprint as UserBluePrint
from flask_smorest import Api
from db import db
import models 
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Shops REST API"
app.config["API_VERSION"] ="v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] ="/"
app.config["OPENAPI_SWAGGER_UI_PATH"] ="/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URL"] = os.getenv("DATABASE_URL", "sqlite:///shop.db")
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "lakshita_sinha"

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return(jsonify({"message": "The token has been revoked", "error": "token_revoked" }), 401)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return(jsonify({"message": "The provided token is expired", "error": "token_expired" }), 401)

@jwt.invalid_token_loader
def invalid_token_loader_callback(error):
    return(jsonify({"message": "Signature verfication failed", "error": "invalid_token" }), 401) 

@jwt.unauthorized_loader
def missing_token_callback(error):
    return(jsonify({"message": "Request does not contain an access token", "error": "authorization_required" }), 401)

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (jsonify(
            {"message": "The token is not fresh",
            "error": "fresh_token_required"
            }
        ), 401)

db.init_app(app)

api= Api(app)

with app.app_context():
    db.create_all()

api.register_blueprint(ShopBluePrint)
api.register_blueprint(ProductBluePrint)
api.register_blueprint(UserBluePrint)
