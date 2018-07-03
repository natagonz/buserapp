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
		if user:
			login_user(user)			
			book = CabTransferBook(car=car,pickup=pickup,drop=drop,price=price,username=form.username.data,email=form.email.data,phone=form.phone.data,date=form.date.data,detail=form.detail.data,status="unpaid",cabtransfer_id=user.id)
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=form.phone.data,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			book = CabTransferBook(car=car,pickup=pickup,drop=drop,price=price,username=form.username.data,email=form.email.data,phone=form.phone.data,date=form.date.data,detail=form.detail.data,status="unpaid",cabtransfer_id=new.id)
			db.session.add(book)
			db.session.commit()
		return redirect(url_for("UserCabTransferPayment",id=book.id))
	return render_template("user/cab/detail.html",form=form,pickup=pickup,drop=drop,price=price,car=car)

@app.route("/cabtransfer/<pickup>/<drop>/request/book",methods=["GET","POST"])
def UserCabTransferRequest(pickup,drop):
	form = CabTransferDetailForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			login_user(user)			
			book = CabTransferBook(car="on request",pickup=pickup,drop=drop,price=0,username=form.username.data,email=form.email.data,phone=form.phone.data,date=form.date.data,detail=form.detail.data,status="on request",cabtransfer_id=user.id)
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=form.phone.data,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			book = CabTransferBook(car="on request",pickup=pickup,drop=drop,price=0,username=form.username.data,email=form.email.data,phone=form.phone.data,date=form.date.data,detail=form.detail.data,status="on request",cabtransfer_id=new.id)
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
	return render_template("user/cab/payment.html",book=book)

