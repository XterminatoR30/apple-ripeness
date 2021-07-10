from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=5, max=50)])
    password = StringField('Password',
                           validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken. Please choose a different one.')
    
    def validate_password(self, password):
        if password.data != current_user.password:
            user = User.query.filter_by(password=password.data).first()
            if user:
                raise ValidationError('Password is already taken. Please choose a different one.')