
@app.route("/charter/<pickup>",methods=["GET","POST"])
def UserCharterTransferCar(pickup):	
	route = CabCharter.query.filter_by(pickup=pickup).first()
	return render_template("user/charter/car.html",route=route,pickup=pickup)

@app.route("/charter/<pickup>/<car>",methods=["GET","POST"])
def UserCharterTransferDetail(pickup,car):
	route = CabCharter.query.filter_by(pickup=pickup).first()
	if car == "micro":
		amount = route.micro
	elif car == "standard":
		amount = route.standard
	elif car == "executive":
		amount = route.executive
	else:
		amount =route.minibus
	
	form = CabCharterDetailForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		phone = str(form.code.data) + str(form.phone.data)
		jam = str(form.jam.data) + " " + str(form.time.data)	
		if user:
			login_user(user)		
			hour = form.hour.data 
			price = amount * int(hour)				
			book = CabCharterBook(jam=jam,car=car,pickup=pickup,price=price,username=form.username.data,hour=hour,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",chartertransfer_id=user.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=phone,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			hour = form.hour.data 
			price = amount * int(hour)	
			book = CabCharterBook(jam=jam,car=car,pickup=pickup,price=price,username=form.username.data,hour=hour,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="unpaid",chartertransfer_id=new.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		return redirect(url_for("UserCharterTransferPayment",id=book.id))
	return render_template("user/charter/detail.html",form=form,pickup=pickup,amount=amount,car=car)


@app.route("/charter/<pickup>/request/book",methods=["GET","POST"])
def UserCharterTransferRequest(pickup):		
	form = CabCharterDetailForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		phone = str(form.code.data) + str(form.phone.data)
		jam = str(form.jam.data) + " " + str(form.time.data)
		if user:
			login_user(user)		
			hour = form.hour.data 						
			book = CabCharterBook(jam=jam,car="on request",pickup=pickup,price=0,username=form.username.data,hour=hour,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="on request",chartertransfer_id=user.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=phone,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			hour = form.hour.data 			
			book = CabCharterBook(jam=jam,car="on request",pickup=pickup,price=0,username=form.username.data,hour=hour,
				email=form.email.data,phone=phone,date=form.date.data,detail=form.detail.data,status="on request",chartertransfer_id=new.id,driver="on request")
			db.session.add(book)
			db.session.commit()
		return redirect(url_for("UserCabTransferNotification"))
	return render_template("user/charter/request.html",form=form,pickup=pickup)


@app.route("/charter/payment/<id>",methods=["GET","POST"])
def UserCharterTransferPayment(id):
	book = CabCharterBook.query.filter_by(id=id).first_or_404()
	secret = str(book.price) + "17cclrc"
	md5 = hashlib.md5(secret).hexdigest()
	return render_template("user/charter/payment.html",book=book,md5=md5)



