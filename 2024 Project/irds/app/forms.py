from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length, Optional, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from app.models import Habitat, Status


class Add_Bird(FlaskForm):
    def check_maximum_lifespan(form, field):
        if field.data < 2:
            raise ValidationError("Birds younger than 2 years are not valid!")
        if field.data > 50:
            raise ValidationError("Birds older than 50 years are not valid!")

    name = StringField('name', validators=[DataRequired(), Length(
        max=20, message="Name cannot exceed 20 characters")])
    maximum_lifespan = IntegerField('maximum_lifespan', validators=[
                                    DataRequired(), check_maximum_lifespan])
    description = TextAreaField('description')
    status = QuerySelectField('Status', query_factory=lambda: Status.query.all(
    ), get_label='name', allow_blank=True, blank_text='Select Status')
    habitats = QuerySelectMultipleField(
        'habitats', query_factory=lambda: Habitat.query.all(), get_label='name')
    

def __init__(self, *args, **kwargs):
    super(Add_Bird, self).__init__(*args, **kwargs)
    self.status.choices = [(status.id, status.name) for status in Status.query.all()]


class SearchBirdForm(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    habitat = QuerySelectField('Habitat', query_factory=lambda: Habitat.query.all(
    ), get_label='name', allow_blank=True, blank_text='Select Habitat')
    submit = SubmitField('Search')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')