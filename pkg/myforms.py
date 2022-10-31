from tkinter import Button
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length


class Itemform(FlaskForm):
    item_name = StringField('Product Name')
    item_price = StringField('Product Price')
    submit = SubmitField('submit')

class Comment(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='Please your message cannot be without a title')])
    content = TextAreaField('Comments', validators=[DataRequired(message='You need to supply the content'), Length(min=10,message='The content cannot be less than 10')])
    post = SubmitField('Post!')