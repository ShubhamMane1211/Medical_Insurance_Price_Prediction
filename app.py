import json
import math
import os
from datetime import datetime

import pandas as pd
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from web.extensions import db, login_manager
from web.forms import LoginForm, PredictionForm, RegisterForm
from web.models import PredictionHistory, User

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(
        __name__,
        template_folder="web/templates",
        static_folder="web/static",
    )
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now().year}

    return app


def register_routes(app: Flask):
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ---------------------------------------------------------------- #
    # Public pages
    # ---------------------------------------------------------------- #
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        form = RegisterForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data.lower()).first()
            if existing_user:
                flash(
                    "An account with that email already exists. Please log in.",
                    "warning",
                )
                return redirect(url_for("login"))

            user = User(name=form.name.data.strip(), email=form.email.data.lower())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash("Account created successfully. Welcome!", "success")
            return redirect(url_for("dashboard"))

        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Logged in successfully.", "success")
                next_page = request.args.get("next")
                return redirect(next_page or url_for("dashboard"))
            flash("Invalid email or password.", "danger")

        return render_template("login.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("index"))

    # ---------------------------------------------------------------- #
    # Prediction
    # ---------------------------------------------------------------- #
    @app.route("/predict", methods=["GET", "POST"])
    @login_required
    def predict():
        form = PredictionForm()
        prediction = None

        if form.validate_on_submit():
            try:
                data = CustomData(
                    age=form.age.data,
                    sex=form.sex.data,
                    bmi=form.bmi.data,
                    children=form.children.data,
                    smoker=form.smoker.data,
                    region=form.region.data,
                )
                features_df = data.get_data_as_data_frame()

                pipeline = PredictPipeline()
                prediction = round(pipeline.predict(features_df), 2)

                record = PredictionHistory(
                    user_id=current_user.id,
                    age=form.age.data,
                    sex=form.sex.data,
                    bmi=form.bmi.data,
                    children=form.children.data,
                    smoker=form.smoker.data,
                    region=form.region.data,
                    predicted_charge=prediction,
                )
                db.session.add(record)
                db.session.commit()

            except Exception as e:
                flash(f"Prediction failed: {e}", "danger")

        return render_template("home.html", form=form, prediction=prediction)

    # ---------------------------------------------------------------- #
    # Dashboard
    # ---------------------------------------------------------------- #
    @app.route("/dashboard")
    @login_required
    def dashboard():
        history = (
            PredictionHistory.query.filter_by(user_id=current_user.id)
            .order_by(PredictionHistory.created_at.desc())
            .all()
        )

        metrics_path = os.path.join(BASE_DIR, "artifacts", "metrics.json")
        metrics = {}
        if os.path.exists(metrics_path):
            with open(metrics_path) as f:
                metrics = json.load(f)

        stats = {
            "total_predictions": len(history),
            "avg_predicted_charge": (
                round(sum(h.predicted_charge for h in history) / len(history), 2)
                if history
                else 0
            ),
            "last_prediction": history[0].created_at.strftime("%b %d, %Y %I:%M %p")
            if history
            else "N/A",
        }

        return render_template(
            "dashboard.html", history=history, metrics=metrics, stats=stats
        )

    # ---------------------------------------------------------------- #
    # JSON APIs used by dashboard charts
    # ---------------------------------------------------------------- #
    @app.route("/api/dataset-summary")
    @login_required
    def api_dataset_summary():
        data_path = os.path.join(BASE_DIR, "artifacts", "data.csv")
        df = pd.read_csv(data_path)

        avg_charge_by_smoker = (
            df.groupby("smoker")["charges"].mean().fillna(0).round(2).to_dict()
        )
        avg_charge_by_region = (
            df.groupby("region")["charges"].mean().fillna(0).round(2).to_dict()
        )
        avg_charge_by_children = (
            df.groupby("children")["charges"]
            .mean()
            .fillna(0)
            .round(2)
            .sort_index()
            .to_dict()
        )

        age_bins = pd.cut(
            df["age"],
            bins=[17, 25, 35, 45, 55, 65, 100],
            labels=["18-25", "26-35", "36-45", "46-55", "56-65", "66+"],
        )
        avg_charge_by_age_group = (
            df.groupby(age_bins, observed=False)["charges"]
            .mean()
            .fillna(0)
            .round(2)
            .to_dict()
        )
        avg_charge_by_age_group = {
            str(k): v for k, v in avg_charge_by_age_group.items()
        }

        bmi_vs_charge_sample = df.sample(min(200, len(df)), random_state=42)[
            ["bmi", "charges", "smoker"]
        ].to_dict(orient="records")

        def clean_nan(obj):
            if isinstance(obj, dict):
                return {k: clean_nan(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_nan(v) for v in obj]
            elif isinstance(obj, float) and math.isnan(obj):
                return None
            return obj

        return jsonify(
            clean_nan(
                {
                    "avg_charge_by_smoker": avg_charge_by_smoker,
                    "avg_charge_by_region": avg_charge_by_region,
                    "avg_charge_by_children": avg_charge_by_children,
                    "avg_charge_by_age_group": avg_charge_by_age_group,
                    "bmi_vs_charge_sample": bmi_vs_charge_sample,
                }
            )
        )

    @app.route("/api/model-scores")
    @login_required
    def api_model_scores():
        metrics_path = os.path.join(BASE_DIR, "artifacts", "metrics.json")
        if not os.path.exists(metrics_path):
            return jsonify({})

        with open(metrics_path) as f:
            metrics = json.load(f)

        return jsonify(metrics.get("all_model_scores", {}))

    @app.route("/api/my-history")
    @login_required
    def api_my_history():
        history = (
            PredictionHistory.query.filter_by(user_id=current_user.id)
            .order_by(PredictionHistory.created_at.asc())
            .all()
        )
        return jsonify(
            [
                {
                    "date": h.created_at.strftime("%Y-%m-%d %H:%M"),
                    "predicted_charge": h.predicted_charge,
                    "age": h.age,
                    "bmi": h.bmi,
                    "smoker": h.smoker,
                }
                for h in history
            ]
        )

    # ---------------------------------------------------------------- #
    # Error handlers
    # ---------------------------------------------------------------- #
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
