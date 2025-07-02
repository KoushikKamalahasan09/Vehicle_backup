from app.routes.auth_routes import bp as auth_bp
from app.routes.admin_routes import bp as admin_bp
from app.routes.users_routes import bp as user_bp
from app.routes.common_routes import bp as common_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(common_bp)

