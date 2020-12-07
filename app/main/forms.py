from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required
from wtforms.validators import Required,Email,EqualTo
from ..models import Mail_list
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

class BlogForm(FlaskForm):

 title = StringField('blog title',validators=[Required()])
 content = TextAreaField('blog')
 image = FileField('Featured Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
 submit = SubmitField('Submit')
 

class CommentForm(FlaskForm):

 comment = TextAreaField('Comment', validators=[Required()])

 submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class SubscribeForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    name = StringField('Enter your full name',validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
            if Mail_list.query.filter_by(email =data_field.data).first():
                raise ValidationError('This email already exists in the mailing list')
