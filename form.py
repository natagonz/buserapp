from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,TextAreaField, IntegerField, DateField, SelectField, SubmitField,FloatField,DecimalField
from wtforms.validators import InputRequired, EqualTo, Email, Length


class RegisterForm(FlaskForm):
	username = StringField("Username",validators=[InputRequired(),Length(max=100)])
	email = StringField("Email",validators=[InputRequired(),Email(),Length(max=100)])
	password = PasswordField("Password",validators=[InputRequired(),Length(min=6,max=100)])

class LoginForm(FlaskForm):
	email = StringField("Email",validators=[InputRequired(),Email(),Length(max=100)])
	password = PasswordField("Password",validators=[InputRequired(),Length(min=6,max=100)])

class UserLoginForm(FlaskForm):
	email = StringField("Email",validators=[InputRequired(),Email(),Length(max=100)])
	
class AddCabTransferRouteForm(FlaskForm):
	pickup = StringField("Pickup",validators=[InputRequired()])
	drop = StringField("Drop",validators=[InputRequired()])
	micro = IntegerField("micro",validators=[InputRequired()])
	standard = IntegerField("standard",validators=[InputRequired()])
	executive = IntegerField("executive",validators=[InputRequired()])
	minibus = IntegerField("minibus",validators=[InputRequired()])

class PickLocationForm(FlaskForm):
	pickup = StringField("Pickup",validators=[InputRequired()])
	drop = StringField("Drop",validators=[InputRequired()])

class PickLocationIndexForm(FlaskForm):
	pickup = StringField("From",validators=[InputRequired()])
	drop = StringField("To",validators=[InputRequired()])


class CabTransferDetailForm(FlaskForm):
	email = StringField("Email",validators=[Email()])
	username = StringField("Username",validators=[InputRequired()])
	phone = StringField("Phone",validators=[InputRequired()])
	date = DateField("Date",format="%m/%d/%Y")
	detail = TextAreaField("Notes")	

class EditCabTransferDetailForm(FlaskForm):
	car = SelectField("Car",choices= [("on request","on request"),("micro","micro"),("standard","standard"),("executive","executive"),("minibus","minibus")])
	price = IntegerField("Price",validators=[InputRequired()])
	date = DateField("Date",format="%m/%d/%Y")
	status =  SelectField("Payment Status",choices= [("on request","on request"),("unpaid","unpaid"),("paid","paid")])

class CabCharterDetailForm(FlaskForm):
	email = StringField("Email",validators=[Email()])
	username = StringField("Username",validators=[InputRequired()])
	phone = StringField("Phone",validators=[InputRequired()])
	date = DateField("Date",format="%m/%d/%Y")
	hour = SelectField("Hour",choices= [("6","6"),("12","12")])
	detail = TextAreaField("Notes")		

class AddVoucherForm(FlaskForm):
	title = StringField("title",validators=[InputRequired()])
	detail = TextAreaField("detail")		
	img = StringField("img url",validators=[InputRequired()])
	price = IntegerField("harga",validators=[InputRequired()])

class VoucherBookForm(FlaskForm):
	email = StringField("Email",validators=[Email()])
	username = StringField("Username",validators=[InputRequired()])
	phone = StringField("Phone",validators=[InputRequired()])
	date = DateField("Date",format="%m/%d/%Y")
	person = IntegerField("Person",validators=[InputRequired()])
	detail = TextAreaField("Notes")			

class EditStatusForm(FlaskForm):
	status =  SelectField("Payment Status",choices= [("on request","on request"),("unpaid","unpaid"),("paid","paid")])
	