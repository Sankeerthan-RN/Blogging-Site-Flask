from wtforms import *
class ArticleForm(Form):
    title = StringField(u'title', validators=[validators.input_required(),validators.length(min=1,max=100)])
    body = TextAreaField(u'body', validators=[validators.input_required(),validators.length(min=10)])