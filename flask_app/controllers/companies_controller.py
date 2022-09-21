from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user_model import user
from flask_app.models.companies_model import Companies
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/user_page")
def all_companies_page():
    if "id" not in session:
        return redirect("/")
    data = {"id": str(session["id"])}
    companies_info = Companies.display_all_companies(session)
    return render_template("/dashboard.html", data = companies_info)


@app.route("/add_new_company")
def add_new_company():
    if "id" not in session:
        return redirect("/")
    return render_template("/new_company_page.html")

@app.route("/save_new_company", methods = ["post"])
def save_new_company():
    if "id" not in session:
        return redirect("/")
    if not Companies.validate_company(request.form):    
        return redirect("/add_new_company")
    symbol = request.form["symbol"]
    if Companies.check_new_comapny(symbol):
        return redirect("/user_page")    
    data = Companies.get_company_info(symbol)
    results = Companies.save_campany(data)
    #this step to save my company for general use
    save_my_company = Companies.save_all_campanies(data)
    return redirect("/user_page")
    

@app.route("/display_company_details/<symbol>")
def display_comopany_details(symbol):
    if "id" not in session:
        return redirect("/")
    data = {"symbol":symbol}
    one_campany_info = Companies.one_company(data)
    return render_template("campany_details.html", data = one_campany_info)

# this part to show all companies in data base 
@app.route("/Show_all_companies")
def show_all_companies():
    if "id" not in session:
        return redirect("/")
    data = Companies.show_all_companies()
    return render_template("all_companies.html", data = data)

@app.route("/Parameters_meanings")
def parameters_meaningS():
    return render_template("parameter_info.html")

@app.route("/update")
def update():
    Companies.update_companies()
    return redirect("/user_page")

@app.route("/delete_company/<int:id>")
def delete_company_info(id):
    if "id" not in session:
        return redirect("/")
    data = {"id":id}
    delete_tv_show = Companies.delete_company(data)
    return redirect("/user_page")
