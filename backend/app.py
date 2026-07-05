from flask import Flask, redirect, url_for

from backend.config import Config

from backend.extensions import (
    db,
    bcrypt,
    login_manager,
    cors
)

from backend.models.user_model import User
from backend.models.resume_model import Resume
from backend.models.interview_model import Interview
from backend.models.result_model import Result
from backend.models.profile_model import Profile
from backend.models.agent_state_model import AgentState

from backend.routes.auth_routes import auth
from backend.routes.resume_routes import resume
from backend.routes.interview_routes import interview
from backend.routes.dashboard_routes import dashboard
from backend.routes.profile_routes import profile
from backend.routes.agent_routes import agent


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(
                User,
                int(user_id)
            )
        except Exception:
            return None

    # Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(resume)
    app.register_blueprint(interview)
    app.register_blueprint(dashboard)
    app.register_blueprint(profile)
    app.register_blueprint(agent)

    @app.route("/")
    def home():
        return redirect(
            url_for("auth.login")
        )

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )