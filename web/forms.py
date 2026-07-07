from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters")]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = SubmitField("Remember Me")
    submit = SubmitField("Log In")


class PredictionForm(FlaskForm):
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=0, max=120)])
    sex = SelectField(
        "Sex", choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()]
    )
    bmi = FloatField("BMI", validators=[DataRequired(), NumberRange(min=5, max=80)])
    children = IntegerField(
        "Number of Children", validators=[DataRequired(), NumberRange(min=0, max=15)]
    )
    smoker = SelectField(
        "Smoker", choices=[("no", "No"), ("yes", "Yes")], validators=[DataRequired()]
    )
    region = SelectField(
        "Region",
        choices=[
            ("northeast", "Northeast"),
            ("northwest", "Northwest"),
            ("southeast", "Southeast"),
            ("southwest", "Southwest"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Predict Charges")
