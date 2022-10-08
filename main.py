import json
import pymysql
from crypt import methods
from enum import unique
from flask_mail import Mail
from re import T
from flask import Flask,render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


pymysql.install_as_MySQLdb()


with open("config.json",'r') as c:
    params = json.load(c)["params"]
local_server = True

db = SQLAlchemy()
app = Flask(__name__)
app.config.update(
    MAIL_SERVER="",
    MAIL_PORT="465",
    MAIL_USE_SSL = True,
    MAIL_USERNAME =params["gmail_username"],
    MAIL_PASSWORD = params["gmail_password"],
)
mail = Mail(app)
# 'mysql://username:password@localhost/db_name'
if(local_server):
    app.config ['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config ['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]
db.init_app(app)


class Contact(db.Model):
   #sno,name,email,phone_num,message,date
   sno = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(100),nullable=False) 
   email = db.Column(db.String(50),nullable=False)
   phone_num = db.Column(db.String(12),nullable=False)
   message = db.Column(db.String(120),nullable=False)
   date = db.Column(db.String(12),nullable=True)

class Posts(db.Model):
   #sno,name,email,phone_num,message,date
   sno = db.Column(db.Integer, primary_key = True)
   title = db.Column(db.String(100),nullable=False) 
   slug = db.Column(db.String(50),nullable=False)
   content = db.Column(db.String(255),nullable=False)
   date = db.Column(db.String(12),nullable=True)
      

@app.route("/")
def home():
    return render_template("index.html",params=params)

@app.route("/about")
def about():
    return render_template("about.html",params=params)

@app.route("/rest")
def rest():
    data = "hellot this is data"
    return jsonify(data=data)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug)
    return render_template("post.html",params=params,post=post)

@app.route("/contact",methods=["GET", "POST"])
def contact():
    if(request.method == "POST"):
        #add data
        #sno,name,email,phone_num,message,date
        name =request.form.get("name")
        email =request.form.get("email")
        phone_num =request.form.get("phone_num")
        message =request.form.get("message")
        entry = Contact(name=name,email=email,phone_num=phone_num,message=message,date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        # mail.send_message('New message from' + name,
        #                 sender=email,
        #                 recipients = params["gmail_username"],pip3 install flask-restful 
        #                 body = message + "\n" + phone_num
        #                 )
    return render_template("contact.html",params=params)

app.run(debug=True)