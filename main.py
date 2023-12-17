from flask import Flask, render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_mail import Mail,Message
import os
# from flask_wtf import StringField,PasswordField,SubmitField
# from flask_wtf.validators import InputRequired,Length,ValidationError
import MySQLdb.cursors
import re
app = Flask(__name__)
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']="anujth678@gmail.com"
app.config['MAIL_PASSWORD']="nuwnhmveyvikswjd"
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE-SSL']=True




app.secret_key="super-secret-key"
bcrypt=Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql://root:@localhost/registration"
db = SQLAlchemy(app)
class infos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname= db.Column(db.String)
    email= db.Column(db.String,  nullable=False)
    password = db.Column(db.String, nullable=True)

class appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    address= db.Column(db.String)
    sickness= db.Column(db.String,  nullable=False)
    preference = db.Column(db.String, nullable=True)
    date= db.Column(db.String,  nullable=False)
    time= db.Column(db.String, nullable=True)



DOC = [{
  'id': 1,
  'name': 'Birendra Sharma',
  'info': 'Heart Surgeon',
  'Email': 'birendrasha444@gmail.com'
}, {
  'id': 2,
  'name': 'Bishal Regmi',
  'info': ' Gynecologists',
  'Email': 'bishalregmi180@gmail.com'
}, {
  'id': 3,
  'name': 'Anuj Thapa',
  'info': 'Ophthalmologists',
  'Email': 'anujth345@gmail.com'
}, {
  'id': 4,
  'name': 'Biswas Kafle',
  'info': 'Otolaryngologists',
  'Email': 'birendrasha444@gmail.com'
}]


@app.route('/',methods=['GET','POST'])
def hello_world():
    #  if request.method=="POST":
    #      msg=Message("hey", sender='anujth678@gmail.com', recipients=['anujth678@gmail.com'])
    #      msg.body="hey buddy how are you?"
    #      mail.send(msg)
    #      return "send email"

     return render_template('home.html', jobs=DOC)

@app.route('/about')
def abouts():
  return render_template('aboutus.html', jobs=DOC)
@app.route('/contact')
def contacts():
  return render_template('contact.html', jobs=DOC)
@app.route('/filling',methods =['GET', 'POST'])
def filling():
    if (request.method=="POST"):
        name=request.form.get('name')
        addresses=request.form.get('address')
        sickness=request.form.get('sickness')
        preference=request.form.get('preference')
        dates=request.form.get('date')
        times=request.form.get('time')
        entry=appointment(name=name, address=addresses, sickness=sickness, preference=preference, date=dates, time=times)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("filling"))
       

#  return render_template("registration.html")    
    return render_template('fills.html', jobs=DOC)
@app.route('/getinfo',methods =['GET', 'POST'])
def getinfo():
    preference=request.form.get('name')
    #users = appointment.query.all()  # Query all users from the database
    users=appointment.query.filter_by(preference=preference)
    return render_template('doctordashboard.html', users=users)  # Pass users data to the HTML template

@app.route('/delete_user', methods=['GET','POST'])
def delete_user():
    users = appointment.query.all()
    user_id = request.form.get('user_id')  # Assuming you're passing user_id as a form parameter

    
        # Retrieve the user from the database
    user = appointment.query.get(user_id)

    if user:
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("doctordashboard"))
    return render_template('doctordashboard.html', users=users)
@app.route('/dashboard',methods =['GET', 'POST'])
def dashboard():
  if "user_id" in session:
     user = infos.query.get(session["user_id"])
     return render_template("dashboard.html", users=user.fname)

  return redirect(url_for("login"))

@app.route('/doctordashboard',methods =['GET', 'POST'])
def doctordashboard():
  if "user_id" in session:
     user = infos.query.get(session["user_id"])
     return render_template("doctordashboard.html", users=user.fname)

  return redirect(url_for("doctorlogin"))

@app.route('/login',methods =['GET', 'POST'])
def login():
    error=None
    if request.method=="POST":
      email=request.form.get('email')
      password=request.form.get('password')
      user=infos.query.filter_by(email=email).first()

      if user and bcrypt.check_password_hash(user.password, password):
         session["user_id"]= user.id
          # login_user(information)
         return redirect(url_for('dashboard'))
      else:
              error="invalid email or password"
              return render_template("login.html",error=error)
    return render_template("login.html")



@app.route('/doctorlogin',methods =['GET', 'POST'])
def doctorlogin():
    error=None
    if request.method=="POST":
      email=request.form.get('email')
      password=request.form.get('password')
      user=infos.query.filter_by(email=email).first()

      if user and bcrypt.check_password_hash(user.password, password):
         session["user_id"]= user.id
          # login_user(information)
         return redirect(url_for('doctordashboard'))
      else:
              error="invalid email or password"
              return render_template("doctorlogin.html",error=error)
    return render_template("doctorlogin.html")
  


@app.route("/register",methods =['GET', 'POST'])
def register():
    if (request.method=="POST"):
        first_name=request.form.get('first')
        last_name=request.form.get('last')
        password=request.form.get('password')
        email=request.form.get('email')
        hashed_password =bcrypt.generate_password_hash(password).decode("utf-8")
        entry=infos(fname=first_name, lname=last_name, email=email, password=hashed_password)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("login"))
       

    return render_template("registration.html")
# @app.route('/register')
# def register():
#   return render_template('registration.html', jobs=DOC)




if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
