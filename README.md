# 🏥 MediPredict - Medical Insurance Price Prediction

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

A production-ready **Machine Learning Web Application** that predicts medical insurance charges based on demographic and health-related attributes.

The application is built using **Python, Flask, Scikit-Learn, Bootstrap 5, SQLite**, and follows an end-to-end Machine Learning workflow including data preprocessing, model training, authentication, dashboards, and interactive visualizations.

---

# 🚀 Features

### Machine Learning

- End-to-End ML Pipeline
- Automated Data Ingestion
- Data Transformation Pipeline
- Feature Engineering
- Model Training & Evaluation
- Hyperparameter Tuning using GridSearchCV
- Automatic Best Model Selection
- Model Serialization using Pickle

### Web Application

- User Registration
- Secure Login & Logout
- Password Hashing
- Prediction History
- Interactive Dashboard
- Responsive Bootstrap UI

### Dashboard Analytics

- Average Charges (Smoker vs Non-Smoker)
- Average Charges by Region
- Average Charges by Age Group
- BMI vs Charges Scatter Plot
- Model Comparison (R² Scores)
- Personal Prediction History

### Production Features

- Custom Exception Handling
- Logging
- Modular Project Structure
- Environment Variable Support
- SQLite Database
- Deployment Ready

---

# 📷 Screenshots

## Home Page

![Home Page](/web/static/images/home.png)
---

## Prediction Page

![Prediction Page](/web/static/images/predict.png)

---

## Dashboard

Prediction Page

![Dashboard](/web/static/images/Dashboard.png)

---

## Analytics



![Charts](/web/static/images/charts.png)

---

# 📂 Project Structure

```text
Medical_Insurance_Prediction/

│
├── artifacts/
├── data/
├── instance/
├── logs/
│
├── src/
│   ├── components/
│   ├── pipeline/
│   ├── logger.py
│   ├── exception.py
│   └── utils.py
│
├── web/
│   ├── templates/
│   ├── static/
│   ├── forms.py
│   ├── models.py
│   └── extensions.py
│
├── app.py
├── application.py
├── requirements.txt
├── setup.py
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Medical_Insurance_Prediction.git

cd Medical_Insurance_Prediction
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Train Model

```bash
python -m src.pipeline.train_pipeline
```

Artifacts generated

```
model.pkl

preprocessor.pkl

metrics.json
```

---

## Run Application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# 📊 Dataset

Dataset contains the following features

| Feature | Description |
|----------|-------------|
| Age | Age of primary beneficiary |
| Sex | Male/Female |
| BMI | Body Mass Index |
| Children | Number of Dependents |
| Smoker | Yes/No |
| Region | Residential Region |
| Charges | Medical Insurance Cost (Target Variable) |

---

# 🤖 Models Evaluated

The following regression algorithms were trained and compared.

- Linear Regression
- Ridge Regression
- Lasso Regression
- K-Nearest Neighbors Regressor
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- AdaBoost Regressor
- Support Vector Regressor (SVR)

The model with the highest **R² Score** is automatically selected and saved.

---

# 📈 Machine Learning Workflow

```
Dataset

↓

Data Ingestion

↓

Train-Test Split

↓

Data Transformation

↓

Feature Scaling

↓

Model Training

↓

Hyperparameter Tuning

↓

Model Evaluation

↓

Best Model Selection

↓

Prediction Pipeline

↓

Flask Application
```

---

# 🔐 Authentication

- User Registration
- Secure Login
- Password Hashing
- Session Management
- Protected Dashboard
- User-specific Prediction History

---

# 📊 Dashboard

The application includes an analytics dashboard containing:

- Model Performance Comparison
- Average Charges by Region
- Average Charges by Age Group
- Smoker vs Non-Smoker Comparison
- BMI vs Charges
- Personal Prediction History

---

# 🛠 Tech Stack

### Backend

- Python
- Flask
- Flask-WTF
- Flask-Login
- Flask-SQLAlchemy

### Machine Learning

- Scikit-Learn
- Pandas
- NumPy

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- Bootstrap Icons
- Chart.js

### Database

- SQLite

---

# 📦 Future Improvements

- Docker Support
- PostgreSQL Integration
- REST API
- Admin Dashboard
- User Profile Management
- Model Retraining from Dashboard
- Cloud Deployment (AWS / Render / Azure)

---

# 👨‍💻 Author

**Shubham Mane**

GitHub: https://github.com/ShubhamMane1211

LinkedIn: https://linkedin.com/in/shubhammane1211
---

# 📄 License

This project is licensed under the MIT License.