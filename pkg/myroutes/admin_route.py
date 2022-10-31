from crypt import methods
from flask import Flask, make_response,render_template,request,redirect,flash, url_for,session
from pkg import app,db
from pkg.mymodels import Admin, Products,User,State
from pkg.myforms import Itemform
from sqlalchemy import desc
from sqlalchemy import or_

@app.route('/admin')
def admin():
    return 'Admin Home'

@app.route('/admin/login', methods=['GET','POST'])
def admin_home():
    if request.method =='GET':
        return render_template('admin/admin_login.html')
    else:
        #retrieve the data
        username= request.form.get('username')
        pwd = request.form.get('password')
        #run a query
        data = db.session.query(Admin).filter(Admin.admin_username == username).filter(Admin.admin_password==pwd).first()
        if data:
            session['adminlogged_in'] = data.admin_id
            """Redirect to the admin dashboard"""
            return redirect('/admin/dashboard')
        else:
            flash('invalid credentials')
            return redirect('/admin/login')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Check if logged in"""
    adminuser = session.get('adminlogged_in')
    if adminuser:
        total_reg = db.session.query(User).count()

        return render_template('admin/admin_dashboard.html', total_reg=total_reg)
    else:
        
        return redirect('/admin/login')

@app.route('/admin/logout')
def admin_logout():
    if session.get('adminlogged_in') !=None:
        session.pop('adminlogged_in')
    return redirect("/admin")
        

@app.route('/admin/product')
def add_product():
    """Check if logged in"""
    adminuser = session.get('adminlogged_in')
    if adminuser:
        all_products = db.session.query(Products).all()

        return render_template('admin/product.html',all_products=all_products)
    else:
        
        return redirect('/admin/login')


@app.route('/admin/new-product',methods=['POST','GET'])
def new_product():
    adminuser = session.get('adminlogged_in')
    if adminuser:
        frm = Itemform()

        if request.method == 'GET':
            return render_template('admin/new_product.html',frm=frm)
        else:
            if frm.validate_on_submit:
                price =frm.item_price.data
                name =frm.item_name.data
                product =Products(product_name=name, product_price=price)
                db.session.add(product)
                db.session.commit()
                flash('Item Succesfully added')
                return redirect('/admin/new-product')
            else:
                return render_template('admin/new_product.html',frm=frm)

        
    else:
        return redirect('/admin/login')

@app.route('/admin/displayuser')
def registereduser():
    """Fetch all the details"""
    adminuser = session.get('adminlogged_in')

    if adminuser:
        #introduced orderby to rearrange stuff - the default is ascending but we can introduce descending
        #regs = db.session.query(User).filter(User.user_fname != 'ize').order_by(User.user_fname.desc())
        regs = db.session.query(User).all()
        statedeets = db.session.query(State).get(3)

        return render_template('admin/displayuser.html',regs=regs,statedeets=statedeets)
    else:
        return redirect('/admin/login')

@app.route('/admin/deleteuser/<id>')
def delete_user(id):
    if session.get('adminlogged_in'):
        user = db.session.query(User).get(id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted')
        return redirect('/admin/displayuser')
    else:
        return redirect('/admin/login')


@app.route('/admin/userdetails/<id>')
def user_details(id):
    if session.get('adminlogged_in'):
        user = db.session.query(User).filter(User.user_id==id)
        return render_template('admin/user_detail.html',user=user)
    else:
        return redirect('/admin/login')
