from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,TextAreaField, IntegerField, DateField, SelectField, BooleanField, SubmitField,FloatField,DecimalField
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
	


class PickLocationForm(FlaskForm):
	pickup = StringField("Pickup",validators=[InputRequired()])
	drop = StringField("Drop",validators=[InputRequired()])

class PickLocationCharter(FlaskForm):
	pickup = StringField("Pickup",validators=[InputRequired()])


class PickLocationIndexForm(FlaskForm):
	pickup = StringField("Where do want to go",validators=[InputRequired()])
	drop = StringField("",validators=[InputRequired()])

class AddCabTransferRouteForm(FlaskForm):
	pickup = StringField("Pickup",validators=[InputRequired()])
	drop = StringField("Drop",validators=[InputRequired()])
	micro = IntegerField("micro",validators=[InputRequired()])
	standard = IntegerField("standard",validators=[InputRequired()])
	executive = IntegerField("executive",validators=[InputRequired()])
	minibus = IntegerField("minibus",validators=[InputRequired()])

class AddCabCharterRouteForm(FlaskForm):
	pickup = StringField("Pickup",validators=[InputRequired()])	
	micro = IntegerField("micro",validators=[InputRequired()])
	standard = IntegerField("standard",validators=[InputRequired()])
	executive = IntegerField("executive",validators=[InputRequired()])
	minibus = IntegerField("minibus",validators=[InputRequired()])	


class CabTransferDetailForm(FlaskForm):
	email = StringField("Email",validators=[Email()])
	username = StringField("Username",validators=[InputRequired()])
	code= SelectField("Country Code",choices=[("93","Afghanistan +93"),("355","Albania +355"),("213","Algeria +213"),
		("376","Andorra +376"),("244","Angola +244"),("672","Antarctica +672"),("54","Argentina +54"),
		("374","Armenia +374"),("61","Australia +61"),("43","Austria +43"),("994","Azerbaijan +994"),
		("973","Bahrain +973"),("880","Bangladesh +880"),("375","Belarus +375"),("32","Belgium +32"),
		("501","Belize +501"),("229","Benin +229"),("975","Bhutan +975"),("591","Bolivia +591"),
		("387","Bosnia and Herzegovina +387"),("267","Botswana +267"),("55","Brazil +55"),
		("673","Brunei +673"),("359","Bulgaria +359"),("226","Burkina Faso +226"),("855","Cambodia +855"),
		("237","Cameroon +237"),("1","Canada +1"),("56","Chile +56"),("86","China +86"),("57","Colombia +57"),
		("506","Costa Rica +506"),("385","Croatia +385"),("357","Cyprus +357"),("420","Czech +420"),("45","Denmark +45"),("670","East Timor +670"),("593","Ecuador +593"),("20","Egypt +20"),("358","Finland +358"),("33","France +33"),("995","Georgia +995"),("49","Germany +49"),("30","Greece +30"),("299","Greenland +299"),("852","Hong Kong +852"),("36","Hungary +36"),("354","Iceland +354"),("91","India +91"),("62","Indonesia +62"),("98","Iran +98"),("964","Iraq +964"),("353","Ireland +353"),("972","Israel +972"),("39","Italy +39"),("81","Japan +81"),("7","Kazakhstan +7"),("965","Kuwait +965"),("956","Laos +856"),("371","Latvia +371"),("218","Libya +218"),("352","Luxembourg +352"),("853","Macau +853"),("60","Malaysia +60"),("52","Mexico +52"),("377","Monaco +377"),("95","Myanmar +95"),("31","Netherlands +31"),("64","New Zealand +64"),("234","Nigeria +234"),("850","North Korea +850"),("47","Norway +47"),("92","Pakistan +92"),("507","Panama +507"),("595","Paraguay +595"),("51","Peru +51"),("63","Philippines +63"),("48","Poland +48"),("351","Portugal +351"),("974","Qatar +974"),("7","Russia +7"),("966","Saudi Arabia +966"),("381","Serbia +381"),("65","Singapore +65"),("421","Slovakia +421"),("386","Slovenia +386"),("27","South Africa +27"),("82","South Korea +82"),("34","spain +34"),("46","Sweden +46"),("41","Switzerland +41"),("963","Syria +963"),("886","Taiwan +886"),("66","Thailand +66"),("90","Turkey +90"),("380","Ukraine +380"),("971","United Arab Emirates +971"),("44","United Kingdom +44"),("1","United States +1"),("598","Uruguay +598"),("998","Uzbekistan +998"),("84","Vietnam +84")])
	phone = StringField("Phone",validators=[InputRequired()])
	date = DateField("Date",format="%m/%d/%Y")
	detail = StringField("How Many Person",validators=[InputRequired()])		
	hour = SelectField("Time",choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),
		("10","10"),("11","11"),("12","12")])
	time = SelectField("Time",choices=[("AM","AM"),("PM","PM")])




class EditCabTransferDetailForm(FlaskForm):
	car = SelectField("Car",choices= [("on request","on request"),("micro","micro"),("standard","standard"),("executive","executive"),("minibus","minibus")])
	price = IntegerField("Price",validators=[InputRequired()])
	date = DateField("Date",format="%m/%d/%Y")
	status =  SelectField("Payment Status",choices= [("on request","on request"),("unpaid","unpaid"),("paid","paid")])
	driver = StringField("Driver")

class CabCharterDetailForm(FlaskForm):
	email = StringField("Email",validators=[Email()])
	username = StringField("Username",validators=[InputRequired()])
	code= SelectField("Country Code",choices=[("93","Afghanistan +93"),("355","Albania +355"),("213","Algeria +213"),
		("376","Andorra +376"),("244","Angola +244"),("672","Antarctica +672"),("54","Argentina +54"),
		("374","Armenia +374"),("61","Australia +61"),("43","Austria +43"),("994","Azerbaijan +994"),
		("973","Bahrain +973"),("880","Bangladesh +880"),("375","Belarus +375"),("32","Belgium +32"),
		("501","Belize +501"),("229","Benin +229"),("975","Bhutan +975"),("591","Bolivia +591"),
		("387","Bosnia and Herzegovina +387"),("267","Botswana +267"),("55","Brazil +55"),
		("673","Brunei +673"),("359","Bulgaria +359"),("226","Burkina Faso +226"),("855","Cambodia +855"),
		("237","Cameroon +237"),("1","Canada +1"),("56","Chile +56"),("86","China +86"),("57","Colombia +57"),
		("506","Costa Rica +506"),("385","Croatia +385"),("357","Cyprus +357"),("420","Czech +420"),("45","Denmark +45"),("670","East Timor +670"),("593","Ecuador +593"),("20","Egypt +20"),("358","Finland +358"),("33","France +33"),("995","Georgia +995"),("49","Germany +49"),("30","Greece +30"),("299","Greenland +299"),("852","Hong Kong +852"),("36","Hungary +36"),("354","Iceland +354"),("91","India +91"),("62","Indonesia +62"),("98","Iran +98"),("964","Iraq +964"),("353","Ireland +353"),("972","Israel +972"),("39","Italy +39"),("81","Japan +81"),("7","Kazakhstan +7"),("965","Kuwait +965"),("956","Laos +856"),("371","Latvia +371"),("218","Libya +218"),("352","Luxembourg +352"),("853","Macau +853"),("60","Malaysia +60"),("52","Mexico +52"),("377","Monaco +377"),("95","Myanmar +95"),("31","Netherlands +31"),("64","New Zealand +64"),("234","Nigeria +234"),("850","North Korea +850"),("47","Norway +47"),("92","Pakistan +92"),("507","Panama +507"),("595","Paraguay +595"),("51","Peru +51"),("63","Philippines +63"),("48","Poland +48"),("351","Portugal +351"),("974","Qatar +974"),("7","Russia +7"),("966","Saudi Arabia +966"),("381","Serbia +381"),("65","Singapore +65"),("421","Slovakia +421"),("386","Slovenia +386"),("27","South Africa +27"),("82","South Korea +82"),("34","spain +34"),("46","Sweden +46"),("41","Switzerland +41"),("963","Syria +963"),("886","Taiwan +886"),("66","Thailand +66"),("90","Turkey +90"),("380","Ukraine +380"),("971","United Arab Emirates +971"),("44","United Kingdom +44"),("1","United States +1"),("598","Uruguay +598"),("998","Uzbekistan +998"),("84","Vietnam +84")])
	phone = StringField("Phone",validators=[InputRequired()])
	date = DateField("Date",format="%m/%d/%Y")
	hour = SelectField("Hour",choices= [("6","6"),("12","12")])
	detail = StringField("How Many Person",validators=[InputRequired()])	
	jam = SelectField("Time",choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),
		("10","10"),("11","11"),("12","12"),])
	time = SelectField("Time",choices=[("AM","AM"),("PM","PM")])
	

class AddVoucherForm(FlaskForm):
	title = StringField("title",validators=[InputRequired()])
	detail = TextAreaField("detail")		
	img = StringField("img url",validators=[InputRequired()])
	price = IntegerField("harga",validators=[InputRequired()])

class VoucherBookForm(FlaskForm):
	email = StringField("Email",validators=[Email()])
	username = StringField("Username",validators=[InputRequired()])
	code= SelectField("Country Code",choices=[("93","Afghanistan +93"),("355","Albania +355"),("213","Algeria +213"),
		("376","Andorra +376"),("244","Angola +244"),("672","Antarctica +672"),("54","Argentina +54"),
		("374","Armenia +374"),("61","Australia +61"),("43","Austria +43"),("994","Azerbaijan +994"),
		("973","Bahrain +973"),("880","Bangladesh +880"),("375","Belarus +375"),("32","Belgium +32"),
		("501","Belize +501"),("229","Benin +229"),("975","Bhutan +975"),("591","Bolivia +591"),
		("387","Bosnia and Herzegovina +387"),("267","Botswana +267"),("55","Brazil +55"),
		("673","Brunei +673"),("359","Bulgaria +359"),("226","Burkina Faso +226"),("855","Cambodia +855"),
		("237","Cameroon +237"),("1","Canada +1"),("56","Chile +56"),("86","China +86"),("57","Colombia +57"),
		("506","Costa Rica +506"),("385","Croatia +385"),("357","Cyprus +357"),("420","Czech +420"),("45","Denmark +45"),("670","East Timor +670"),("593","Ecuador +593"),("20","Egypt +20"),("358","Finland +358"),("33","France +33"),("995","Georgia +995"),("49","Germany +49"),("30","Greece +30"),("299","Greenland +299"),("852","Hong Kong +852"),("36","Hungary +36"),("354","Iceland +354"),("91","India +91"),("62","Indonesia +62"),("98","Iran +98"),("964","Iraq +964"),("353","Ireland +353"),("972","Israel +972"),("39","Italy +39"),("81","Japan +81"),("7","Kazakhstan +7"),("965","Kuwait +965"),("956","Laos +856"),("371","Latvia +371"),("218","Libya +218"),("352","Luxembourg +352"),("853","Macau +853"),("60","Malaysia +60"),("52","Mexico +52"),("377","Monaco +377"),("95","Myanmar +95"),("31","Netherlands +31"),("64","New Zealand +64"),("234","Nigeria +234"),("850","North Korea +850"),("47","Norway +47"),("92","Pakistan +92"),("507","Panama +507"),("595","Paraguay +595"),("51","Peru +51"),("63","Philippines +63"),("48","Poland +48"),("351","Portugal +351"),("974","Qatar +974"),("7","Russia +7"),("966","Saudi Arabia +966"),("381","Serbia +381"),("65","Singapore +65"),("421","Slovakia +421"),("386","Slovenia +386"),("27","South Africa +27"),("82","South Korea +82"),("34","spain +34"),("46","Sweden +46"),("41","Switzerland +41"),("963","Syria +963"),("886","Taiwan +886"),("66","Thailand +66"),("90","Turkey +90"),("380","Ukraine +380"),("971","United Arab Emirates +971"),("44","United Kingdom +44"),("1","United States +1"),("598","Uruguay +598"),("998","Uzbekistan +998"),("84","Vietnam +84")])
	phone = StringField("Phone",validators=[InputRequired()])
	date = DateField("Date",format="%m/%d/%Y")
	person = SelectField("Pax",choices= [("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9")])	
	detail = TextAreaField("Notes")			

class EditStatusForm(FlaskForm):
	status =  SelectField("Payment Status",choices= [("on request","on request"),("unpaid","unpaid"),("paid","paid")])

class BodyguardPriceForm(FlaskForm):
	price = IntegerField("harga",validators=[InputRequired()])

class AddBuserDriverForm(FlaskForm):
	email = StringField("Email",validators=[Email()])
	username = StringField("Name",validators=[InputRequired()])
	phone = StringField("Phone",validators=[InputRequired()])
	region = SelectField("Region",choices= [("Buleleng","Buleleng"),("Denpasar","Denpasar"),("Badung","Badung"),
		("Tabanan","Tabanan"),("Gianyar","Gianyar"),("Bangli","Bangli"),("Karang Asem","Karang Asem"),("Jembrana","Jembrana")
		,("Klungkung","Klungkung")])
	

class EditBuserDriverForm(FlaskForm):
	email = StringField("Email",validators=[Email()])
	username = StringField("Name",validators=[InputRequired()])
	phone = StringField("Phone",validators=[InputRequired()])
	region = SelectField("Region",choices= [("Buleleng","Buleleng"),("Denpasar","Denpasar"),("Badung","Badung"),
		("Tabanan","Tabanan"),("Gianyar","Gianyar"),("Bangli","Bangli"),("Karang Asem","Karang Asem"),("Jembrana","Jembrana")
		,("Klungkung","Klungkung")])
	status =  SelectField("Status",choices= [("non aktif","non aktif"),("aktif","aktif")])	


class FilterDriverForm(FlaskForm):
	region = SelectField("Region",choices= [("Buleleng","Buleleng"),("Denpasar","Denpasar"),("Badung","Badung"),
		("Tabanan","Tabanan"),("Gianyar","Gianyar"),("Bangli","Bangli"),("Karang Asem","Karang Asem"),("Jembrana","Jembrana")
		,("Klungkung","Klungkung")])
	status =  SelectField("Status",choices= [("non aktif","non aktif"),("aktif","aktif")])	


class AddLocationForm(FlaskForm):
	location = StringField("Location",validators=[InputRequired()])


class AddTravelAgentForm(FlaskForm):
	email = StringField("Email",validators=[Email()])
	username = StringField("Name",validators=[InputRequired()])
	phone = StringField("Phone",validators=[InputRequired()])
	


class CharterBookForm(FlaskForm):
	pickup = StringField("Pickup",validators=[InputRequired()])
	email = StringField("Email",validators=[Email()])
	username = StringField("Username",validators=[InputRequired()])
	code= SelectField("Country Code",choices=[("93","Afghanistan +93"),("355","Albania +355"),("213","Algeria +213"),
		("376","Andorra +376"),("244","Angola +244"),("672","Antarctica +672"),("54","Argentina +54"),
		("374","Armenia +374"),("61","Australia +61"),("43","Austria +43"),("994","Azerbaijan +994"),
		("973","Bahrain +973"),("880","Bangladesh +880"),("375","Belarus +375"),("32","Belgium +32"),
		("501","Belize +501"),("229","Benin +229"),("975","Bhutan +975"),("591","Bolivia +591"),
		("387","Bosnia and Herzegovina +387"),("267","Botswana +267"),("55","Brazil +55"),
		("673","Brunei +673"),("359","Bulgaria +359"),("226","Burkina Faso +226"),("855","Cambodia +855"),
		("237","Cameroon +237"),("1","Canada +1"),("56","Chile +56"),("86","China +86"),("57","Colombia +57"),
		("506","Costa Rica +506"),("385","Croatia +385"),("357","Cyprus +357"),("420","Czech +420"),("45","Denmark +45"),("670","East Timor +670"),("593","Ecuador +593"),("20","Egypt +20"),("358","Finland +358"),("33","France +33"),("995","Georgia +995"),("49","Germany +49"),("30","Greece +30"),("299","Greenland +299"),("852","Hong Kong +852"),("36","Hungary +36"),("354","Iceland +354"),("91","India +91"),("62","Indonesia +62"),("98","Iran +98"),("964","Iraq +964"),("353","Ireland +353"),("972","Israel +972"),("39","Italy +39"),("81","Japan +81"),("7","Kazakhstan +7"),("965","Kuwait +965"),("956","Laos +856"),("371","Latvia +371"),("218","Libya +218"),("352","Luxembourg +352"),("853","Macau +853"),("60","Malaysia +60"),("52","Mexico +52"),("377","Monaco +377"),("95","Myanmar +95"),("31","Netherlands +31"),("64","New Zealand +64"),("234","Nigeria +234"),("850","North Korea +850"),("47","Norway +47"),("92","Pakistan +92"),("507","Panama +507"),("595","Paraguay +595"),("51","Peru +51"),("63","Philippines +63"),("48","Poland +48"),("351","Portugal +351"),("974","Qatar +974"),("7","Russia +7"),("966","Saudi Arabia +966"),("381","Serbia +381"),("65","Singapore +65"),("421","Slovakia +421"),("386","Slovenia +386"),("27","South Africa +27"),("82","South Korea +82"),("34","spain +34"),("46","Sweden +46"),("41","Switzerland +41"),("963","Syria +963"),("886","Taiwan +886"),("66","Thailand +66"),("90","Turkey +90"),("380","Ukraine +380"),("971","United Arab Emirates +971"),("44","United Kingdom +44"),("1","United States +1"),("598","Uruguay +598"),("998","Uzbekistan +998"),("84","Vietnam +84")])
	phone = StringField("Phone",validators=[InputRequired()])
	date = DateField("Date",format="%m/%d/%Y")
	hour = SelectField("Hour",choices= [("3","3"),("5","5"),("8","8"),("10","10"),("12","12")])
	detail = StringField("How Many Person",validators=[InputRequired()])	
	jam = SelectField("Time",choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),
		("10","10"),("11","11"),("12","12"),])
	time = SelectField("Time",choices=[("AM","AM"),("PM","PM")])