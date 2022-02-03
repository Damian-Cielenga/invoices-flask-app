from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Login')
    remember = BooleanField("Remember Me")

class ResetForm(FlaskForm):
    username        = StringField('Username',validators=[DataRequired(), Length(min=2, max=40)])
    email           = StringField('E-mail',validators=[DataRequired(), Email()])
    submit_password = SubmitField("Reset Password")