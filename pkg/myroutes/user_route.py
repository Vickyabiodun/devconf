
from flask import Flask, make_response,render_template,request,redirect,flash, url_for,session,jsonify,json
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app,db,csrf
from pkg.mymodels import Post, User,State,Products,Purchase,Comment,Lga,Transaction
import os,random,string
import requests
from pkg.myforms import Comment
 

@app.route('/home',methods=['POST','GET'])
def hompage():
    response= requests.get('http://127.0.0.1:8088/api/V1/listall')
    """Pick the json within the response object above"""
    rsp = response.json()
    return render_template('user/home.html',rsp=rsp)



@app.route('/signup',methods=['POST','GET'])
def user_signup():
    if request.method == 'GET':

        return render_template('user/regform.html')
    else:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        enc_password = generate_password_hash(password)
        u = User(user_fname=fname, user_lname=lname,user_email=email,user_pass=enc_password)
        db.session.add(u)
        db.session.commit()
        id=u.user_id
        if id != None:
            flash('Thank you for joining')
        return redirect ('/login')

@app.route('/login',methods=['POST','GET'])
def user_login():
    if request.method == 'GET':
        return render_template('user/user_login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        """Method 1"""
        record = db.session.query(User).filter(User.user_email==username).first()
        """You can pass record to a test template to see the contents"""
        if record and check_password_hash(record.user_pass,password):           
            session['loggedin']=record.user_id
            return redirect('/dashboard')  
        else:
            flash('Failed login')
            return redirect('/login')

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    loggedin = session.get('loggedin')  

    record = db.session.query(User).filter(User.user_id==loggedin).first()
    return render_template('user/user_dashboard.html',first=record.user_fname)  

@app.route('/dashboard',methods=['POST','GET'])
def logout():
    if session.get('user_login') != None:
        session.pop('user_login')
    return redirect("url_for('user_home')")          

@app.route('/update-profile', methods=['POST','GET'])
def update_profile():
    if session.get('loggedin') !=None:
        if request.method =='GET':
            deets = db.session.query(User).filter(User.user_id==session.get('loggedin')).first()
            states = db.session.query(State).all()

            return render_template('user/update_profile.html',deets=deets,states=states)
        else:
            #to upload image
            fileobj= request.files['pic']
            allowed =['.jpg','.png','.jpeg']
            error =[]
            newfilename=''
            if fileobj.filename !='':

                original_name = fileobj.filename
                filename,ext = os.path.splitext(original_name)
                """Check if extension is allowed"""
                if ext.lower() in allowed:
                    """Generate a random name"""
                    newfilename = random.random()
                    xter_list = random.sample(string.ascii_letters,12)
                    newfilename = ''.join(xter_list) + ext
                    fileobj.save(f'pkg/static/upload/{original_name}')
                else:
                    error.append('Extension not allowed')
            else:
                error.append('Extension not allowed')


            fname= request.form.get('fname')
            lname= request.form.get('lname')
            state= request.form.get('state')
            phone= request.form.get('phone')
            userobj = db.session.query(User).filter(User.user_id==session.get('loggedin')).first()
            
            userobj.user_fname =fname
            userobj.user_lname= lname
            userobj.user_state= state
            userobj.user_phone= phone
            userobj.user_image = newfilename
            db.session.commit()
            return redirect('/update-profile')
    else:
        return redirect('/login')
@app.route('/store', methods=['POST','GET'] )
def store():
    if session.get('loggedin') !=None:
        if request.method == 'GET':
            user_products = Products.query.all()
            #user_products= Products.query.all()
            loggedin = session.get('loggedin')

            return render_template('user/store.html', user_products=user_products,loggedin =loggedin)
        else:
            userid = session.get('loggedin')

            '''Generate a transation ref no and keep it in a session variable'''
            refno = int(random.random() * 1000000000)
            session['tref'] = refno

            '''Insert into Transaction Table'''
            trans = Transaction(trx_user=userid,trx_refno=refno,trx_status='pending',trx_method='cash')            
            db.session.add(trans) 
            db.session.commit()
            '''Get the id from transaction table and insert into purchases table'''
            id = trans.trx_id
            
            '''Before you insert new purchases, delete existing ones first'''
           
            db.session.execute(f'delete from purchase where purchase_userid ="{userid}"')
            db.session.commit()
            productid= request.form.getlist('productid')
            total_amt = 0
            for p in productid:
                pobj = Purchase(purchase_userid=session.get('loggedin'),purchase_productid=p, purchase_trxid = id)
                db.session.add(pobj)
                db.session.commit()
                product_amt = pobj.productdeets.product_price
                total_amt = total_amt+ product_amt

            '''UPDATE the total amount on transaction table with product_amt'''

            trans.trx_totalamt = total_amt
            db.session.commit()
            return redirect('/confirm')
    else:
        return redirect('/login')


@app.route('/confirm', methods=['POST','GET'] )
def confirm_purchases():
    userid = session.get('loggedin')
    transaction_ref = session.get('tref')
    if userid !=None:
        '''Retrieve all the things this user has selected from Purchases table
        save it in a variable and Then send it to the template'''        
        data = db.session.query(Purchase).join(Transaction).filter(Transaction.trx_refno==transaction_ref).all()       
        return render_template('user/confirmpurchases.html',data=data)
    else:
        return redirect('/login')

@app.route('/conversation')
def conversation():
    if session.get('loggedin') !=None:
        """A query to fetch everything from the posts table"""
        all_post = Post.query.order_by(Post.post_date.desc()).all()
        return render_template('user/conversations.html',all_post=all_post)
    else:
        return redirect('/login')

@app.route('/theconversations/<id>',methods=['POST','GET'])
def theconversations(id):
    if session.get('loggedin') !=None:
        if request.method == "GET":
            """A query to fetch everything from the posts table"""
            all_post = db.session.query(Post).get_or_404(id)
            return render_template('user/theconversations.html',all_post=all_post)
        else:
            com = request.form.get('comment')
            userid= session.get('loggedin')
            comment = Comment(comment_by= userid, comment_content=com,comment_postid =id)
            db.session.add(comment)
            db.session.commit()

            data = {'madeby':'ggg', "comment":com}

            data_json = jsonify(data)
            return data_json

@app.route('/makepost',methods=['POST','GET'])
def makepost():
    if session.get('loggedin') !=None:
        postform = Comment()
        if request.method =='GET':
            """A query to fetch everything from the posts table"""
            return render_template('user/posts.html', postform=postform)
        else:
            if postform.validate_on_submit():
                title = request.form.get('title')
                content= request.form.get('content')
                newpost = Post(post_content=content, post_title=title,post_userid =session.get('loggedin'))
                db.session.add(newpost)
                db.session.commit()
                if newpost.post_id>0:
                    flash('post succesfully crerated')
                    return redirect('/conversation')
                else:
                    flash('Ooops, your comment was not added')
                    return render_template('user/posts.html', postform=postform)
            else:
                return render_template('user/posts.html', postform=postform)
    else:
        return redirect('/login')

@app.route('/getlga')
def getlga():
    if session.get('loggedin') !=None:
        stateid = request.args.get('stateid')
        opt=''
        """A query taht gets lga where stateid = stateid"""
        rows = db.session.query(Lga).filter(Lga.state_id == stateid).all()
        for r in rows:
            opt = opt + f'<option>{r.lga_name}</option>'
        return opt

@app.route('/ajax/check_email_form')
def check_email_form():
        return render_template('user/check_email.html')
 
@app.route('/ajax/check_email')
def check_email():
    useremail = request.get('email')
    row= db.session.query(User).filter(User.user_email == useremail).first()
    if row:
        return 'Email adress in use already'
    else:
        return 'email address available'

@app.route("/insert_comment")
def insert_comment():
    comment = request.form.get('comment')

@app.route("/paystack_response")
def paystack_response():
    return 'Paystack will send us response here as a JSON'

@app.route("/paystack_step1",methods=['POST','GET'])
def paystack():
    userid = session.get('loggedin')
    if userid != None:
        url = "https://api.paystack.co/transaction/initialize"
        '''Retrieve the user's email address, amount in kobo , refno '''
        userdeets = User.query.get(userid)
        deets = Transaction.query.filter(Transaction.trx_refno==session.get('tref')).first()
        '''Construct the json we are sending to PAYSTACK API'''

        data = {"email":userdeets.user_email,"amount":deets.trx_totalamt*100, "reference":deets.trx_refno}
        '''SET the authorization '''
        headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_c05cde60482e485f43866fb9668dad1d36d9c486"}

        response = requests.post(url, headers=headers, data=json.dumps(data))
        rspjson = json.loads(response.text) 

        return render_template('user/test.html',rspjson=rspjson)
    return 'Paystack will send us response here as a JSON'