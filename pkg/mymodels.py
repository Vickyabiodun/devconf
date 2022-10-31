import datetime
from pkg import db


class State(db.Model): 
    __tablename___='tbl_state'
    state_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)
class Products(db.Model): 
    product_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_price = db.Column(db.Float(), nullable=False)

class User(db.Model): 
    user_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user_email = db.Column(db.String(255), nullable=False)
    user_pass = db.Column(db.String(255), nullable=False)
    user_fname = db.Column(db.String(255), nullable=False)
    user_lname = db.Column(db.String(255), nullable=False)
    user_state = db.Column(db.Integer(),db.ForeignKey('state.state_id'), nullable=True)
    user_phone = db.Column(db.String(100), nullable=True)
    user_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    user_image = db.Column(db.String(255), nullable=False)
    mystate = db.relationship('State',backref='theusers')


class Transaction(db.Model):
    trx_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    trx_user = db.Column(db.Integer(),db.ForeignKey('user.user_id'), nullable=False)
    trx_refno= db.Column(db.String(255), nullable=True)
    trx_totalamt = db.Column(db.Float(), nullable=True)
    trx_status = db.Column(db.Enum('pending','paid','failed'), nullable=True)
    trx_method=db.Column(db.Enum('card','cash'), nullable=True)
    trx_paygate=db.Column(db.Text(), nullable=True)
    trx_date=db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    
    user_whopaid = db.relationship('User',backref='purchases_de')

class Admin(db.Model): 
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_username = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)
    admin_lastlogin = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow)

class Purchase(db.Model): 
    purchase_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    purchase_userid = db.Column(db.Integer(),db.ForeignKey('user.user_id'), nullable=False)
    purchase_productid = db.Column(db.Integer(),db.ForeignKey('products.product_id'), nullable=False)
    purchase_trxid = db.Column(db.Integer(),db.ForeignKey('transaction.trx_id'), nullable=False)
    
    productdeets = db.relationship('Products',backref='prods')
    userdetails = db.relationship('User',backref='myusers')
    transdeets= db.relationship('Transaction',backref='purchases_deets')

class Post(db.Model): 
    post_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    post_content = db.Column(db.Text(), nullable=False)
    post_date = db.Column(db.DateTime(), default= datetime.datetime.utcnow())
    post_title = db.Column(db.String(255), nullable=False)
    post_userid = db.Column(db.Integer(),db.ForeignKey('user.user_id'), nullable=False)
    """To set up relationship between user and posts"""
    postrel = db.relationship('User',backref='userspost')

class Comment(db.Model): 
    comment_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    comment_postid = db.Column(db.Integer(),db.ForeignKey('post.post_id'), nullable=False)
    comment_content = db.Column(db.Text(), nullable=False)
    comment_by = db.Column(db.Integer(),db.ForeignKey('user.user_id'), nullable=False)
    comment_date = db.Column(db.DateTime(), default= datetime.datetime.utcnow())
    """To set up relationship btw comment and post and btw user and comment"""
    commentby = db.relationship('User',backref='comments')
    commentpost = db.relationship('Post',backref='mycomments')

class Lga(db.Model): 
    lga_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_id = db.Column(db.Integer(),db.ForeignKey('state.state_id'), nullable=False )
    lga_name = db.Column(db.String(255), nullable=False)
    thestate = db.relationship('State',backref='lgadeets')


class Plang(db.Model):
    plang_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    plang_name = db.Column(db.String(255), nullable=False)
    plang_description = db.Column(db.String(255), nullable=False)


class Userlang(db.Model):
    userlang_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    """To set up the foreign key"""
    userlang_plang =  db.Column(db.Integer(),db.ForeignKey('plang.plang_id'), nullable=False)
    userlang_user =  db.Column(db.Integer(),db.ForeignKey('user.user_id'), nullable=False)
    langdeet = db.relationship('Plang',backref='langs')
    userdeet = db.relationship('User',backref='users')
