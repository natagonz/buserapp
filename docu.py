@app.route("/dashboard/admin/voucher",methods=["GET","POST"])
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
		if user:
			login_user(user)		
			person = form.person.data 
			price = voucher.price * int(person)				
			book = VoucherBook(title=voucher.title,price=price,username=form.username.data,person=person,
				email=form.email.data,phone=form.phone.data,date=form.date.data,detail=form.detail.data,status="unpaid",voucher_id=user.id)
			db.session.add(book)
			db.session.commit()
		else :
			new = User(username=form.username.data,email=form.email.data,phone=form.phone.data,role="user")
			db.session.add(new)
			db.session.commit()
			login_user(new)	
			person = form.person.data 
			price = voucher.price * int(person)				
			book = VoucherBook(title=voucher.title,price=price,username=form.username.data,person=person,
				email=form.email.data,phone=form.phone.data,date=form.date.data,detail=form.detail.data,status="unpaid",voucher_id=new.id)
			db.session.add(book)
			db.session.commit()
		return redirect(url_for("UserVoucherPayment",id=book.id))
	return render_template("user/voucher/detail.html",form=form,voucher=voucher)		


@app.route("/voucher/payment/<id>",methods=["GET","POST"])
def UserVoucherPayment(id):
	voucher = VoucherBook.query.filter_by(id=id).first_or_404()
	return render_template("user/voucher/payment.html",voucher=voucher)
