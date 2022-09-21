from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user_model import user
from flask_app.models.companies_model import Companies
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods = ["post"])
def register():
    if not user.validate_register(request.form):
        return redirect("/")
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])}
    results = user.register_function(data)
    session["id"] = results
    session["name"] = data["first_name"]
    return redirect("/user_page")

@app.route("/login", methods = ["post"])
def login():
    data ={"email": request.form['email']}
    user_info = user.get_by_email(data)
    if not user_info:
        flash("Your email or password are Invalid. please enter valid email and password", "login")
        return redirect("/")
    if not  bcrypt.check_password_hash(user_info.password, request.form['password']):
        flash("Your email or password are Invalid. please enter valid email and password", "login")
        return redirect("/")
    else:
        session["id"] = user_info.id
        session["name"] = user_info.first_name
    return redirect("/user_page")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

