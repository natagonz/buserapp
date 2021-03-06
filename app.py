# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
from config import database, secret
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_login import LoginManager , UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_mail import Mail,Message 
from functools import wraps
from form import UserLoginForm,RegisterForm,LoginForm,PickLocationForm,EditStatusForm,PickLocationIndexForm,AddCabTransferRouteForm
from form import CabTransferDetailForm,EditCabTransferDetailForm,CabCharterDetailForm,AddVoucherForm,VoucherBookForm,BodyguardPriceForm,AddBuserDriverForm,EditBuserDriverForm,FilterDriverForm
from form import AddLocationForm,AddCabCharterRouteForm,PickLocationCharter,AddTravelAgentForm,CharterBookForm
import hashlib
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,TextAreaField, IntegerField, DateField, SelectField, SubmitField,FloatField,DecimalField
from wtforms.validators import InputRequired, EqualTo, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField


app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config["SECRET_KEY"] = secret 
db = SQLAlchemy(app)
app.debug = True 



class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100))
	email = db.Column(db.String(200))
	phone = db.Column(db.String(100)) 
	password = db.Column(db.String(500))	
	role = db.Column(db.String(100))	
	cabtransfer = db.relationship("CabTransferBook",backref="cabtransfer",lazy="dynamic")
	chartertransfer = db.relationship("CabCharterBook",backref="chartertransfer",lazy="dynamic")
	voucher = db.relationship("VoucherBook",backref="voucher",lazy="dynamic")
	bodyguard = db.relationship("BodyGuardBook",backref="bodyguard",lazy="dynamic")
	
	def is_active(self):
		return True

	def get_id(self):
		return self.id

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False

class Location(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	location = db.Column(db.String(200))

	def __repr__(self):
		return '{}'.format(self.location)

def location_query():
	return Location.query.all()	


class CabTransfer(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	pickup = db.Column(db.Text())
	drop = db.Column(db.Text())
	micro = db.Column(db.Integer())
	standard = db.Column(db.Integer())
	executive = db.Column(db.Integer())
	minibus = db.Column(db.Integer())		

class CabTransferBook(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(200))
	username = db.Column(db.String(200))
	phone = db.Column(db.String(200))	
	date = db.Column(db.DateTime())	
	detail = db.Column(db.Text())	
	pickup = db.Column(db.String(200))
	drop = db.Column(db.String(200))	
	car = db.Column(db.String(200))	
	price = db.Column(db.Integer())	
	status = db.Column(db.String(200))
	driver = db.Column(db.String(200))
	hour = db.Column(db.String(200))	
	cabtransfer_id = db.Column(db.Integer(), db.ForeignKey("user.id"))


class CabCharter(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	pickup = db.Column(db.Text())	
	micro = db.Column(db.Integer())
	standard = db.Column(db.Integer())
	executive = db.Column(db.Integer())
	minibus = db.Column(db.Integer())	

class CabCharterBook(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(200))
	username = db.Column(db.String(200))
	phone = db.Column(db.String(200))	
	date = db.Column(db.DateTime())	
	detail = db.Column(db.Text())	
	pickup = db.Column(db.String(200))	
	car = db.Column(db.String(200))	
	price = db.Column(db.Integer())
	hour = db.Column(db.Integer())
	status = db.Column(db.String(200))	
	driver = db.Column(db.String(200))
	jam = db.Column(db.String(200))	
	chartertransfer_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

class Voucher(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(200))
	detail = db.Column(db.UnicodeText())
	img = db.Column(db.UnicodeText())
	price = db.Column(db.BigInteger())

class VoucherBook(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(200))
	email = db.Column(db.String(200))
	username = db.Column(db.String(200))
	phone = db.Column(db.String(200))	
	date = db.Column(db.DateTime())	
	detail = db.Column(db.Text())	
	price = db.Column(db.Integer())
	person = db.Column(db.Integer())
	status = db.Column(db.String(200))	
	voucher_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

class BodyGuardBook(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(200))
	email = db.Column(db.String(200))
	username = db.Column(db.String(200))
	phone = db.Column(db.String(200))	
	date = db.Column(db.DateTime())	
	detail = db.Column(db.Text())	
	price = db.Column(db.Integer())
	person = db.Column(db.Integer())
	status = db.Column(db.String(200))	
	bodyguard_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

class BodyGuardPrice(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	price = db.Column(db.Integer())

class BuserDriver(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(200))
	email = db.Column(db.String(200))
	phone = db.Column(db.String(200))
	region = db.Column(db.String(200))
	status = db.Column(db.String(200))



class TravelAgent(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(200))
	email = db.Column(db.String(200))
	phone = db.Column(db.String(200))




#################################################### Decorator ##############################################################################

#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "Login"

#user loader
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))

#fungsi mail
app.config.from_pyfile("config.py") 
mail = Mail(app)
s = URLSafeTimedSerializer("secret")



@app.route("/",methods=["GET","POST"])
def Index():
	form = PickLocationIndexForm()
	if form.validate_on_submit():
		pickup = form.pickup.data 
		drop = form.drop.data 
		route = CabTransfer.query.filter_by(pickup=pickup,drop=drop).first()
		if route:
			return redirect(url_for("UserCabTransferCar",pickup=pickup,drop=drop))
		else :
			return redirect(url_for("UserCabTransferRequest",pickup=pickup,drop=drop))	
	return render_template("index.html",form=form)

################################################# Auth route #########################################################
@app.route("/admin/register",methods=["GET","POST"])
def AdminRegister():	 
	form = RegisterForm()
	if form.validate_on_submit():
		hass = generate_password_hash(form.password.data,method="sha256")
		admin = User(username=form.username.data,email=form.email.data,password=hass,role="admin")
		db.session.add(admin)
		db.session.commit()

		login_user(admin)
		return redirect(url_for("AdminDashboard"))
	return render_template("auth/admin_register.html",form=form)

@app.route("/admin/login",methods=["GET","POST"])
def AdminLogin():
	form = LoginForm()
	if form.validate_on_submit():
		admin = User.query.filter_by(email=form.email.data).first()
		if admin :
			if check_password_hash(admin.password,form.password.data):
				login_user(admin)
				return redirect(url_for("AdminDashboard"))
		flash("invalid login","danger")
	return render_template("auth/admin_login.html",form=form)

@app.route("/dashboard/admin",methods=["GET","POST"])
@login_required
def AdminDashboard():
	return render_template("admin/dashboard/index.html")


@app.route("/login",methods=["GET","POST"])
def UserLogin():
	form = UserLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and user.role == "user":
			login_user(user)
			return redirect(url_for("UserDashboard"))
		else :
			flash("invalid login")
	return render_template("auth/login.html",form=form)			






############################################################# Cab Transfer ##########################################
@app.route("/dashboard/admin/cab",methods=["GET","POST"])
@login_required
def AdminCab():
	return render_template("admin/cab/cab.html")

@app.route("/dashboard/admin/cab/route",methods=["GET","POST"])
@login_required
def AdminCabRoute():
	routes = CabTransfer.query.all()
	form = AddCabTransferRouteForm()
	if form.validate_on_submit():
		pickup = form.pickup.data
		drop = form.drop.data 
		
		rute = CabTransfer(pickup=pickup,drop=drop,micro=form.micro.data,standard=form.standard.data,executive=form.executive.data,minibus=form.minibus.data)	
		db.session.add(rute)
		db.session.commit()

		flash("rute berhasil ditambah","success")
		return redirect(url_for("AdminCabRoute"))
	return render_template("admin/cab/route.html",form=form,routes=routes)

@app.route("/dashboard/admin/cab/route/<id>",methods=["GET","POST"])
@login_required
def AdminCabRouteEdit(id):
	routes = CabTransfer.query.all()
	form = AddCabTransferRouteForm()
	cab = CabTransfer.query.filter_by(id=id).first()
	form.pickup.data = cab.pickup
	form.drop.data = cab.drop
	form.micro.data = cab.micro
	form.standard.data = cab.standard
	form.executive.data = cab.executive
	form.minibus.data = cab.minibus
	if form.validate_on_submit():
		pickup = request.form["pickup"]
		drop = request.form["drop"]
		
		cab.pickup = pickup
		cab.drop = drop
		cab.micro = request.form["micro"]
		cab.standard = request.form["standard"]
		cab.executive = request.form["executive"]
		cab.minibus = request.form["minibus"]
		db.session.commit()

		flash("rute berhasil di edit","success")
		return redirect(url_for("AdminCabRoute"))	
	return render_template("admin/cab/route.html",form=form,routes=routes)

@app.route("/dashboard/admin/cab/route/<id>/delete",methods=["GET","POST"])
@login_required
def AdminCabRouteDelete(id):
	cab = CabTransfer.query.filter_by(id=id).first()
	db.session.delete(cab)
	db.session.commit()
	flash("rute berhasil di hapus","success")
	return redirect(url_for("AdminCabRoute"))	

@app.route("/dashboard/admin/cab/book",methods=["GET","POST"])
@login_required
def AdminCabBookAll():
	books = CabTransferBook.query.all()
	return render_template("admin/cab/book.html",books=books)

@app.route("/dashboard/admin/cab/book/<id>",methods=["GET","POST"])
@login_required
def AdminCabBookEdit(id):
	book = CabTransferBook.query.filter_by(id=id).first_or_404()
	form = EditCabTransferDetailForm()
	form.status.data = book.status
	form.price.data = book.price
	form.car.data = book.car
	form.date.data = book.date 
	form.driver.data = book.driver
	if form.validate_on_submit():
		book.car = request.form["car"]
		book.price = request.form["price"]
		book.status = request.form["status"]
		date = datetime.strptime(request.form["date"], '%m/%d/%Y').strftime('%Y-%m-%d')	
		book.date = date 
		book.driver = request.form["driver"]
		db.session.commit()
		flash("data berhasil di update","success")
		return redirect(url_for("AdminCabBookAll"))
	return render_template("admin/cab/edit.html",book=book,form=form)

@app.route("/dashboard/admin/cab/book/invoice/<id>",methods=["GET","POST"])
@login_required
def AdminCabBook(id):
	book = CabTransferBook.query.filter_by(id=id).first_or_404()
	return render_template("admin/cab/invoice.html",book=book)




@app.route("/dashboard/admin/cab/book/delete/<id>",methods=["GET","POST"])
@login_required
def AdminCabBookDelete(id):
	book = CabTransferBook.query.filter_by(id=id).first_or_404()
	db.session.delete(book)
	db.session.commit()
	flash("data berhasil dihapus","success")
	return redirect(url_for("AdminCabBookAll"))



@app.route("/cabtransfer",methods=["GET","POST"])
def UserCabTransfer():
	form = PickLocationForm()
	if form.validate_on_submit():
		pickup = form.pickup.data 
		drop = form.drop.data 
		route = CabTransfer.query.filter_by(pickup=pickup,drop=drop).first()
		if route:
			return redirect(url_for("UserCabTransferCar",pickup=pickup,drop=drop))
		else :
			return redirect(url_for("UserCabTransferRequest",pickup=pickup,drop=drop))			
	return render_template("user/cab/cab.html",form=form)

@app.route("/cabtransfer/<pickup>/<drop>",methods=["GET","POST"])
def UserCabTransferCar(pickup,drop):	
	route = CabTransfer.query.filter_by(pickup=pickup,drop=drop).first()
	return render_template("user/cab/car.html",route=route,pickup=pickup,drop=drop)		

@app.route("/cabtransfer/<pickup>/<drop>/<car>",methods=["GET","POST"])
def UserCabTransferDetail(pickup,drop,car):
	route = CabTransfer.query.filter_by(pickup=pickup,drop=drop).first()
	if car == "micro":
		price = route.micro
	elif car == "standard":
		price = route.standard
	elif car == "executive":
		price = route.executive
	else:
		price =route.minibus
	
	form = CabTransferDetailForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		phone = str(form.code.data) + str(form.phone.data)
		hour = str(form.hour.data) + " " + str(form.time.data)	
		if user:
			login_user(user)			
			book = CabTransferBook(hour=hour,car=car,pickup=pickup,drop=drop,price=price,username=form.username.data,email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",cabtransfer_id=user.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=phone,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			book = CabTransferBook(hour=hour,car=car,pickup=pickup,drop=drop,price=price,username=form.username.data,email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",cabtransfer_id=new.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		return redirect(url_for("UserCabTransferPayment",id=book.id))
	return render_template("user/cab/detail.html",form=form,pickup=pickup,drop=drop,price=price,car=car)

@app.route("/cabtransfer/<pickup>/<drop>/request/book",methods=["GET","POST"])
def UserCabTransferRequest(pickup,drop):
	form = CabTransferDetailForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		phone = str(form.code.data) + str(form.phone.data)
		hour = str(form.hour.data) + " " + str(form.time.data)	
		if user:
			login_user(user)			
			book = CabTransferBook(hour=hour,car="on request",pickup=pickup,drop=drop,price=0,username=form.username.data,email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="on request",cabtransfer_id=user.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=phone,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			book = CabTransferBook(hour=hour,car="on request",pickup=pickup,drop=drop,price=0,username=form.username.data,email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="on request",cabtransfer_id=new.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		return redirect(url_for("UserCabTransferNotification"))
	return render_template("user/cab/request.html",form=form,pickup=pickup,drop=drop)		

@app.route("/cabtransfer/request/notification",methods=["GET","POST"])
@login_required
def UserCabTransferNotification():
	return render_template("user/cab/notification.html")

@app.route("/cabtransfer/<id>",methods=["GET","POST"])
def UserCabTransferPayment(id):
	book = CabTransferBook.query.filter_by(id=id).first_or_404()
	secret = str(book.price) + "17cclrc"
	md5 = hashlib.md5(secret).hexdigest()
	return render_template("user/cab/payment.html",book=book,md5=md5)


################################################# Cab Charter ##############################################
@app.route("/dashboard/admin/charter",methods=["GET","POST"])
@login_required
def AdminCharter():
	return render_template("admin/charter/charter.html")

@app.route("/dashboard/admin/charter/route",methods=["GET","POST"])
@login_required
def AdminCharterRoute():
	routes = CabCharter.query.all()
	form = AddCabCharterRouteForm()
	if form.validate_on_submit():
		pickup = form.pickup.data		 
		#check
		check = CabTransfer.query.filter_by(pickup=pickup).first()
		if check:
			flash("Rute sudah ada","danger")
		else :
			rute = CabCharter(pickup=pickup,micro=form.micro.data,standard=form.standard.data,executive=form.executive.data,minibus=form.minibus.data)	
			db.session.add(rute)
			db.session.commit()

			flash("rute berhasil ditambah","success")
			return redirect(url_for("AdminCharterRoute"))
	return render_template("admin/charter/route.html",form=form,routes=routes)

@app.route("/dashboard/admin/charter/route/<id>",methods=["GET","POST"])
@login_required
def AdminCharterEdit(id):
	routes = CabCharter.query.all()
	form = AddCabCharterRouteForm()
	cab = CabCharter.query.filter_by(id=id).first()
	form.pickup.data = cab.pickup	
	form.micro.data = cab.micro
	form.standard.data = cab.standard
	form.executive.data = cab.executive
	form.minibus.data = cab.minibus
	if form.validate_on_submit():
		pickup = request.form["pickup"]	
		#check
		check = CabCharter.query.filter_by(pickup=pickup).all()
		if len(check) > 1:
			flash("Rute sudah ada","danger")
		else :
			cab.pickup = pickup			
			cab.micro = request.form["micro"]
			cab.standard = request.form["standard"]
			cab.executive = request.form["executive"]
			cab.minibus = request.form["minibus"]
			db.session.commit()

			flash("rute berhasil di edit","success")
			return redirect(url_for("AdminCharterRoute"))	
	return render_template("admin/charter/route.html",form=form,routes=routes)

@app.route("/dashboard/admin/charter/route/<id>/delete",methods=["GET","POST"])
@login_required
def AdminCharterRouteDelete(id):
	cab = CabCharter.query.filter_by(id=id).first()
	db.session.delete(cab)
	db.session.commit()
	flash("rute berhasil di hapus","success")
	return redirect(url_for("AdminCharterRoute"))	

@app.route("/dashboard/admin/charter/book",methods=["GET","POST"])
@login_required
def AdminCharterBookAll():
	books = CabCharterBook.query.all()
	return render_template("admin/charter/book.html",books=books)

@app.route("/dashboard/admin/charter/book/<id>",methods=["GET","POST"])
@login_required
def AdminCharterBookEdit(id):
	book = CabCharterBook.query.filter_by(id=id).first_or_404()
	form = EditCabTransferDetailForm()
	form.status.data = book.status
	form.price.data = book.price
	form.car.data = book.car
	form.date.data = book.date 
	form.driver.data = book.driver
	if form.validate_on_submit():
		book.car = request.form["car"]
		book.price = request.form["price"]
		book.status = request.form["status"]
		date = datetime.strptime(request.form["date"], '%m/%d/%Y').strftime('%Y-%m-%d')	
		book.date = date 
		driver = request.form["driver"]
		db.session.commit()
		flash("data berhasil di update","success")
		return redirect(url_for("AdminCharterBookAll"))
	return render_template("admin/charter/edit.html",book=book,form=form)


@app.route("/dashboard/admin/charter/book/invoice/<id>",methods=["GET","POST"])
@login_required
def AdminCharterBook(id):
	book = CabCharterBook.query.filter_by(id=id).first_or_404()
	return render_template("admin/charter/invoice.html",book=book)


@app.route("/dashboard/admin/charter/book/delete/<id>",methods=["GET","POST"])
@login_required
def AdminCharterBookDelete(id):
	book = CabCharterBook.query.filter_by(id=id).first_or_404()
	db.session.delete(book)
	db.session.commit()
	flash("data berhasil dihapus","success")
	return redirect(url_for("AdminCharterBookAll"))


#revisi
@app.route("/charter",methods=["GET","POST"])
def UserCharterTransfer():
	form = CharterBookForm()
	if form.validate_on_submit():
		pickup = form.pickup.data 		
		route = CabCharter.query.filter_by(pickup=pickup).first()
		user = User.query.filter_by(email=form.email.data).first()
		phone = str(form.code.data) + str(form.phone.data)
		jam = str(form.jam.data) + " " + str(form.time.data)
		hour = form.hour.data 	
		if user:
			login_user(user)											
			book = CabCharterBook(jam=jam,car="on request",pickup=pickup,price=0,username=form.username.data,hour=hour,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",chartertransfer_id=user.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=phone,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			
			book = CabCharterBook(jam=jam,car="on request",pickup=pickup,price=0,username=form.username.data,hour=hour,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",chartertransfer_id=new.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		
		if route:
			return redirect(url_for("UserCharterTransferCar",pickup=pickup,id=book.id))
		else :
			return redirect(url_for("UserCabTransferNotification"))			
	return render_template("user/charter/charter.html",form=form)


@app.route("/charter/<pickup>/<id>",methods=["GET","POST"])
@login_required
def UserCharterTransferCar(pickup,id):
	route = CabCharter.query.filter_by(pickup=pickup).first()
	book = CabCharterBook.query.filter_by(id=id).first()
	return render_template("user/charter/car.html",route=route,pickup=pickup,book=book)


@app.route("/charter/<pickup>/<car>/<id>",methods=["GET","POST"])
def UserCharterTransferDetail(pickup,car,id):
	route = CabCharter.query.filter_by(pickup=pickup).first()
	if car == "micro":
		amount = route.micro
	elif car == "standard":
		amount = route.standard
	elif car == "executive":
		amount = route.executive
	else:
		amount =route.minibus

	book = CabCharterBook.query.filter_by(id=id).first()
	hour = int(book.hour)
	price = amount * hour
	book.price = price
	book.car = car 
	db.session.commit()
	
	return redirect(url_for("UserCharterTransferPayment",id=id))


@app.route("/charter/payment/<id>",methods=["GET","POST"])
def UserCharterTransferPayment(id):
	book = CabCharterBook.query.filter_by(id=id).first_or_404()
	secret = str(book.price) + "17cclrc"
	md5 = hashlib.md5(secret).hexdigest()
	return render_template("user/charter/payment.html",book=book,md5=md5)



##################################################### Voucher ####################################################
@app.route("/dashboard/admin/voucher",methods=["GET","POST"])
@login_required
def VoucherIndex():
	return render_template("admin/voucher/voucher.html")


@app.route("/dashboard/admin/voucher/all",methods=["GET","POST"])
@login_required
def AllVoucher():
	vouchers = Voucher.query.all()
	form = AddVoucherForm()
	if form.validate_on_submit():
		voucher = Voucher(title=form.title.data,detail=form.detail.data,price=form.price.data,img=form.img.data)
		db.session.add(voucher)
		db.session.commit()
		flash("voucher berhasil di tambah","success")
		return redirect(url_for("AllVoucher"))
	return render_template("admin/voucher/all.html",vouchers=vouchers,form=form)

@app.route("/dashboard/admin/voucher/<id>/edit",methods=["GET","POST"])
@login_required
def VoucherEdit(id):
	vouchers = Voucher.query.all()
	voucher = Voucher.query.filter_by(id=id).first_or_404()
	form = AddVoucherForm()
	form.title.data = voucher.title
	form.img.data = voucher.img
	form.detail.data = voucher.detail
	form.price.data = voucher.price
	if form.validate_on_submit():
		voucher.title = request.form["title"]
		voucher.img = request.form["img"]
		voucher.price = request.form["price"]
		voucher.detail = request.form["detail"]
		db.session.commit()
		flash("voucher berhasil diperbaharui","success")
		return redirect(url_for("AllVoucher"))
	return render_template("admin/voucher/edit.html",form=form,vouchers=vouchers)	

@app.route("/dashboard/admin/voucher/<id>/delete",methods=["GET","POST"])
@login_required
def VoucherDelete(id):
	voucher = Voucher.query.filter_by(id=id).first_or_404()
	db.session.delete(voucher)
	db.session.commit()
	flash("voucher berhasil diperbaharui","success")
	return redirect(url_for("AllVoucher"))

@app.route("/dashboard/admin/voucher/book",methods=["GET","POST"])
@login_required
def AllVoucherBook():
	books = VoucherBook.query.all()
	return render_template("admin/voucher/book.html",books=books)

@app.route("/dashboard/admin/voucher/book/<id>",methods=["GET","POST"])
@login_required
def VoucherBookEdit(id):
	book = VoucherBook.query.filter_by(id=id).first_or_404()
	form = EditStatusForm()
	form.status.data = book.status
	if form.validate_on_submit():
		book.status = request.form["status"]
		db.session.commit()

		flash("Data berhasil di update","success")
		return redirect(url_for("AllVoucherBook"))
	return render_template("admin/voucher/edit_status.html",form=form,book=book)	

@app.route("/dashboard/admin/voucher/book/invoice/<id>",methods=["GET","POST"])
@login_required
def AdminVoucherInvoice(id):
	book = VoucherBook.query.filter_by(id=id).first_or_404()
	return render_template("admin/voucher/invoice.html",book=book)

@app.route("/dashboard/admin/voucher/book/delete/<id>",methods=["GET","POST"])
@login_required
def AdminVoucherBookDelete(id):
	book = VoucherBook.query.filter_by(id=id).first_or_404()
	db.session.delete(book)
	db.session.commit()
	flash("data berhasil dihapus","success")
	return redirect(url_for("AllVoucherBook"))


@app.route("/voucher",methods=["GET","POST"])
def UserAllVoucher():
	vouchers = Voucher.query.all()	
	return render_template("user/voucher/all.html",vouchers=vouchers)


@app.route("/voucher/<id>",methods=["GET","POST"])
def VoucherId(id):
	voucher = Voucher.query.filter_by(id=id).first_or_404()
	return render_template("user/voucher/voucher.html",voucher=voucher)

@app.route("/voucher/book/<id>",methods=["GET","POST"])
def UserVoucherBook(id):
	voucher = Voucher.query.filter_by(id=id).first_or_404()
	form = VoucherBookForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		phone = str(form.code.data) + str(form.phone.data)
		if user:
			login_user(user)		
			person = form.person.data 
			price = voucher.price * int(person)				
			book = VoucherBook(title=voucher.title,price=price,username=form.username.data,person=person,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",voucher_id=user.id)
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=phone,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			person = form.person.data 
			price = voucher.price * int(person)				
			book = VoucherBook(title=voucher.title,price=price,username=form.username.data,person=person,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",voucher_id=new.id)
			db.session.add(book)
			db.session.commit()
		return redirect(url_for("UserVoucherPayment",id=book.id))
	return render_template("user/voucher/detail.html",form=form,voucher=voucher)		


@app.route("/voucher/payment/<id>",methods=["GET","POST"])
def UserVoucherPayment(id):
	voucher = VoucherBook.query.filter_by(id=id).first_or_404()
	secret = str(voucher.price) + "17cclrc"
	md5 = hashlib.md5(secret).hexdigest()
	return render_template("user/voucher/payment.html",voucher=voucher,md5=md5)


################################################## Body Guard ########################################
@app.route("/dashboard/admin/bodyguard",methods=["GET","POST"])
@login_required
def BodyGuardRoute():
	return render_template("admin/bodyguard/bodyguard.html")


@app.route("/dashboard/admin/bodyguard/price/<id>",methods=["GET","POST"])
@login_required
def AddBodyGuardPrice(id):
	form = BodyguardPriceForm()
	price = BodyGuardPrice.query.filter_by(id=id).first_or_404()
	form.price.data = price.price
	if form.validate_on_submit():
		price.price = request.form["price"]
		db.session.commit()
		flash("harga bodyguard berhasil di rubah","success")
		return redirect(url_for("AddBodyGuardPrice",id=id))
	return render_template("admin/bodyguard/price.html",form=form,price=price)	


@app.route("/bodyguard",methods=["GET","POST"])
def UserBodyGuardBook():	
	form = VoucherBookForm()
	bodyguard = BodyGuardPrice.query.first()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()	
		phone = str(form.code.data) + str(form.phone.data)	
		if user:
			login_user(user)		
			person = form.person.data 
			price = bodyguard.price * int(person)	
			title = "Bodyguard Services"			
			book = BodyGuardBook(title=title,price=price,username=form.username.data,person=person,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",bodyguard_id=user.id)
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=phone,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			person = form.person.data 
			price = bodyguard.price * int(person)
			title = "Bodyguard Services"				
			book = BodyGuardBook(title=title,price=price,username=form.username.data,person=person,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",bodyguard_id=new.id)
			db.session.add(book)
			db.session.commit()
		return redirect(url_for("UserBodyGuardPayment",id=book.id))
	return render_template("user/bodyguard/detail.html",form=form,bodyguard=bodyguard)

@app.route("/bodyguard/payment/<id>",methods=["GET","POST"])
def UserBodyGuardPayment(id):
	book = BodyGuardBook.query.filter_by(id=id).first_or_404()	
	secret = str(book.price) + "17cclrc"
	md5 = hashlib.md5(secret).hexdigest()
	return render_template("user/bodyguard/payment.html",book=book,md5=md5)


@app.route("/dashboard/admin/bodyguard/book",methods=["GET","POST"])
@login_required
def AllBodyGuardBook():
	books = BodyGuardBook.query.all()	
	return render_template("admin/bodyguard/book.html",books=books)

@app.route("/dashboard/admin/bodyguard/book/<id>",methods=["GET","POST"])
@login_required
def VoucherBodyGuardEdit(id):
	book = BodyGuardBook.query.filter_by(id=id).first_or_404()
	form = EditStatusForm()
	form.status.data = book.status
	if form.validate_on_submit():
		book.status = request.form["status"]
		db.session.commit()

		flash("Data berhasil di update","success")
		return redirect(url_for("AllBodyGuardBook"))
	return render_template("admin/bodyguard/edit_status.html",form=form,book=book)	


@app.route("/dashboard/admin/bodyguard/book/invoice/<id>",methods=["GET","POST"])
@login_required
def AdminBodyGuardInvoice(id):
	book = BodyGuardBook.query.filter_by(id=id).first_or_404()
	return render_template("admin/bodyguard/invoice.html",book=book)	


@app.route("/dashboard/admin/bodyguard/book/delete/<id>",methods=["GET","POST"])
@login_required
def AdminBodyGuardBookDelete(id):
	book = BodyGuardBook.query.filter_by(id=id).first_or_404()
	db.session.delete(book)
	db.session.commit()
	flash("data berhasil dihapus","success")
	return redirect(url_for("AllBodyGuardBook"))



############################################################ User Dashboard ################################
@app.route("/dashboard/user",methods=["GET","POST"])
@login_required
def UserDashboard():
	cabs = CabCharterBook.query.filter_by(chartertransfer_id=current_user.id).all() 
	vouchers = VoucherBook.query.filter_by(voucher_id=current_user.id).all()
	transfers = CabTransferBook.query.filter_by(cabtransfer_id=current_user.id).all()
	bodys = BodyGuardBook.query.filter_by(bodyguard_id=current_user.id).all()
	return render_template("user/dashboard/dashboard.html",cabs=cabs,vouchers=vouchers,transfers=transfers,bodys=bodys)






######################################################## Driver ###########################################
@app.route("/driver",methods=["GET","POST"])
def AddBuserDriver():
	form = AddBuserDriverForm()
	if form.validate_on_submit():
		driver = BuserDriver(username=form.username.data,email=form.email.data,phone=form.phone.data,region=form.region.data,status="non aktif")
		db.session.add(driver)
		db.session.commit()
		return redirect(url_for("DriverConfirmation"))
	return render_template("user/driver/add.html",form=form)	

@app.route("/driver/confirmation",methods=["GET","POST"])
def DriverConfirmation():
	return render_template("user/driver/confirmation.html")


@app.route("/dashboard/admin/driver",methods=["GET","POST"])
@login_required
def AllDriver():
	drivers = BuserDriver.query.all()
	return render_template("admin/driver/all.html",drivers=drivers)


@app.route("/dashboard/admin/driver/<id>",methods=["GET","POST"])
@login_required
def EditDriver(id):
	drivers = BuserDriver.query.all()
	form = EditBuserDriverForm()
	driver = BuserDriver.query.filter_by(id=id).first()
	form.username.data = driver.username
	form.email.data = driver.email
	form.phone.data = driver.phone
	form.region.data = driver.region
	form.status.data = driver.status
	if form.validate_on_submit():
		driver.username = request.form["username"]
		driver.email = request.form["email"]
		driver.phone = request.form["phone"]
		driver.region = request.form["region"]
		driver.status = request.form["status"]

		db.session.commit()
		flash("Driver berhasil di update","success")
		return redirect(url_for("AllDriver"))
	return render_template("admin/driver/edit.html",form=form,drivers=drivers)	


@app.route("/dashboard/admin/driver/delete/<id>",methods=["GET","POST"])
@login_required
def DeleteDriver(id):
	driver = BuserDriver.query.filter_by(id=id).first()
	db.session.delete(driver)
	db.session.commit()
	flash("Driver berhasil di hapus","success")
	return redirect(url_for("AllDriver"))


@app.route("/dashboard/admin/driver/filter",methods=["GET","POST"])
@login_required
def FilterDriver():
	form = FilterDriverForm()
	drivers = BuserDriver.query.all()
	if form.validate_on_submit():		
		status = form.status.data 
		region = form.region.data 
		return redirect(url_for("DriverResult",status=status,region=region))
	return render_template("admin/driver/filter.html",form=form,drivers=drivers)	


@app.route("/dashboard/admin/driver/<status>/<region>",methods=["GET","POST"])
@login_required
def DriverResult(status,region):
	drivers = BuserDriver.query.filter_by(status=status,region=region).all()
	return render_template("admin/driver/all.html",drivers=drivers)






@app.route("/travelagent",methods=["GET","POST"])
def TravelAgentRegister():
	form = AddTravelAgentForm()
	if form.validate_on_submit():
		travel = TravelAgent(username=form.username.data,email=form.email.data,phone=form.phone.data)
		db.session.add(travel)
		db.session.commit()
		flash("Terima kasih,anda aka segera di hubungi","success")
		return redirect(url_for("DriverConfirmation"))
	return render_template("user/travel/form.html",form=form)		


@app.route("/dashboard/admin/agent",methods=["GET","POST"])
@login_required
def AllTravelAgent():
	drivers = TravelAgent.query.all()
	return render_template("user/travel/all.html",drivers=drivers)




################################################ Buser Adz ############################
@app.route("/buseradz",methods=["GET","POST"])
def BuserAdzIndex():
	return render_template("buseradz/index.html")



















if __name__ == "__main__":
	app.run(host='0.0.0.0')
