from wtforms import *
class RegisterForm(Form):
    first_name = StringField(u'First Name', validators=[validators.input_required(),validators.length(min=1,max=30)])
    last_name  = StringField(u'Last Name', validators=[validators.optional()])
    email = StringField('Email',[validators.Length(min=4,max=25)])
    username=StringField(u'Username', validators=[validators.input_required(),validators.length(min=1,max=30)])
    password = PasswordField('Password', [ validators.input_required(),validators.EqualTo('confirm',message ='passwords do not match')])
    confirm = PasswordField('Confirm password')