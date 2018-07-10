from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class DrinkForm(FlaskForm):
    choices = [("Drink name", "Drink name"), ("Ingredient", "Ingredient")]
    select = SelectField("Search by:", choices= choices)
    search = StringField('', validators= [DataRequired()])
    submit = SubmitField("Search")


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField('Sign In')