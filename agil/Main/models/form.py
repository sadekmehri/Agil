from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    Email = EmailField('Email', id="email", validators=[DataRequired()])
    Cin = StringField('Cin', id="cin", validators=[DataRequired()])
    Password = PasswordField('Password', id="Password", validators=[DataRequired()])
    Remember = BooleanField('Remember me')


class ForgetForm(FlaskForm):
    Cin = EmailField('Cin', id="cin", validators=[DataRequired()])


class ResetLoginForm(FlaskForm):
    Password = PasswordField('Password', validators=[DataRequired()])
