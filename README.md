# 🏥 MediPredict — Medical Insurance Price Prediction

A production-ready end-to-end machine learning web application that predicts
annual **medical insurance charges** based on a person's age, sex, BMI,
number of children, smoking status, and region. Built with **Flask**,
**Scikit-Learn**, and **Bootstrap 5**, with user authentication and an
interactive analytics dashboard.

---

## ✨ Features

- **ML pipeline** — modular data ingestion → transformation → model training
  components, trained on 9 candidate regression models with hyperparameter
  search via `GridSearchCV`, auto-selecting the best performer by R² score.
- **Authentication** — secure signup/login with hashed passwords
  (`Flask-Login` + `Werkzeug`), session management, and per-user prediction
  history stored in SQLite.
- **Prediction UI** — a clean Bootstrap form that calls the trained model and
  returns an instant estimated charge.
- **Dashboard & Charts** — Chart.js visualizations for:
  - Average charges: smoker vs non-smoker
  - Average charges by region
  - Average charges by age group
  - BMI vs charges scatter plot
  - Model comparison (R² across all trained models)
  - Your personal prediction history over time
- **Production practices** — custom exception handling, structured logging,
  `.pkl` artifact persistence, config via environment variables, WSGI entry
  point for deployment (Gunicorn / Elastic Beanstalk).

---

## 📂 Project Structure

```
MLPROJECT/
│
├── artifacts/                     # Generated at training time
│   ├── data.csv                   # Cleaned full dataset
│   ├── train.csv / test.csv       # Train/test split
│   ├── model.pkl                  # Best trained model
│   ├── preprocessor.pkl           # Fitted ColumnTransformer
│   └── metrics.json               # Model evaluation report
│
├── data/
│   └── insurance.csv              # Raw source dataset
│
├── logs/                          # Rotating run logs (gitignored)
│
├── src/
│   ├── exception.py               # CustomException with file/line context
│   ├── logger.py                  # App-wide logger configuration
│   ├── utils.py                   # save/load objects, model evaluation helpers
│   │
│   ├── components/
│   │   ├── data_ingestion.py      # Reads CSV, cleans, splits train/test
│   │   ├── data_transformation.py # Builds & fits preprocessing pipeline
│   │   └── model_trainer.py       # Trains, tunes, selects best model
│   │
│   └── pipeline/
│       ├── train_pipeline.py      # Orchestrates the full training run
│       └── predict_pipeline.py    # Loads artifacts, serves predictions
│
├── templates/                     # Jinja2 + Bootstrap templates
│   ├── base.html, index.html
│   ├── login.html, register.html
│   ├── home.html                  # Prediction form
│   ├── dashboard.html             # Charts & history
│   └── errors/404.html, 500.html
│
├── static/
│   ├── css/style.css
│   └── js/dashboard.js            # Chart.js rendering logic
│
├── extensions.py                  # Flask-SQLAlchemy / Flask-Login instances
├── models.py                      # User, PredictionHistory ORM models
├── forms.py                       # WTForms: Register / Login / Prediction
├── app.py                         # Flask app factory + all routes
├── application.py                 # WSGI entry point for deployment
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Clone & create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the model

This reads `data/insurance.csv`, runs the full ingestion → transformation →
training pipeline, and writes `model.pkl`, `preprocessor.pkl`, and
`metrics.json` into `artifacts/`.

```bash
python -m src.pipeline.train_pipeline
```

Expected output:
```
Best model: Random Forest Regressor | R2 score: 0.90
```

### 4. Run the app

```bash
python app.py
```

Visit **http://localhost:5000**, sign up for an account, and start predicting.

### 5. Production deployment

```bash
gunicorn application:application
```

Set these environment variables in production:

| Variable       | Purpose                                  |
|----------------|-------------------------------------------|
| `SECRET_KEY`   | Flask session/CSRF signing key            |
| `DATABASE_URL` | SQLAlchemy DB URI (defaults to SQLite)    |

---

## 🧠 Dataset

The model is trained on `data/insurance.csv` (2,772 records) with columns:

| Column     | Type    | Description                          |
|------------|---------|----------------------------------------|
| `age`      | int     | Age of primary beneficiary             |
| `sex`      | string  | `male` / `female`                      |
| `bmi`      | float   | Body mass index                        |
| `children` | int     | Number of dependents                   |
| `smoker`   | string  | `yes` / `no`                           |
| `region`   | string  | `northeast`, `northwest`, `southeast`, `southwest` |
| `charges`  | float   | **Target** — annual medical charges ($)|

## 🤖 Model Training Details

`ModelTrainer` evaluates the following regressors with grid-searched
hyperparameters, and persists the highest scoring one:

- Linear Regression, Ridge, Lasso
- K-Neighbors Regressor
- Decision Tree
- Random Forest Regressor
- Gradient Boosting Regressor
- AdaBoost Regressor
- SVR

Preprocessing (`DataTransformation`) scales numeric features
(`age`, `bmi`, `children`) with `StandardScaler` and one-hot encodes
categorical features (`sex`, `smoker`, `region`).

## 🔐 Authentication

- Passwords are hashed with Werkzeug's `generate_password_hash` — never
  stored in plaintext.
- Sessions are managed by `Flask-Login`.
- All prediction and dashboard routes are protected with `@login_required`.
- Each user only ever sees their own prediction history.

## 📊 API Endpoints (used internally by the dashboard)

| Endpoint                  | Description                                   |
|----------------------------|------------------------------------------------|
| `GET /api/dataset-summary` | Aggregated dataset stats for charts           |
| `GET /api/model-scores`    | R² score per trained candidate model          |
| `GET /api/my-history`      | Current user's prediction history (JSON)      |

## 🛠 Tech Stack

- **Backend**: Flask, Flask-Login, Flask-SQLAlchemy, Flask-WTF
- **ML**: Scikit-Learn, Pandas, NumPy, dill
- **Frontend**: Bootstrap 5, Bootstrap Icons, Chart.js
- **Database**: SQLite (swap `DATABASE_URL` for Postgres/MySQL in production)

## 📄 License

MIT — feel free to use and adapt this project.
