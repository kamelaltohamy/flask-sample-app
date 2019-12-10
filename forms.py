from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators  import DataRequired, Length
from wtforms.widgets  import TextArea

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired(), Length(min=6)])


class SnapForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()])
    extension = StringField('extension',validators=[DataRequired()])
    content= StringField('content',widget=TextArea(),validators=[DataRequired()])
    