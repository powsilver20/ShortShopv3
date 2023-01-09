from flask import Flask,request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import sqlite3
import os
import requests
import uuid


app = Flask(__name__)

currentlocation = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/login/<type>",methods=["POST"])
def checklogin(type):

    UN = request.form['email_address']
    PW = request.form['password']
    sqlconnection = sqlite3.Connection(currentlocation + "/database/users.db")
    cursor = sqlconnection.cursor()

    query1 = f"SELECT * From {type} WHERE email = '{UN}' AND password = '{PW}'"
    cursor.execute(query1)
    rows = cursor.fetchall()
    if (len(rows)) ==1 and (type == "buyer"):
        return render_template("feed.html")

    if (len(rows)) == 1 and (type == "seller"):
        return redirect(f"/seller/home/{UN}")
        return render_template("seller-create-listing.html")

    else:
        return redirect(f"/login/{type}")

@app.route("/seller/home/<id>",methods=['POST', 'GET'])
def sellerhome(id):
    if request.method == 'POST':
        image = request.files['file']
        product_name = request.form['product-name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        if image and product_name and description and price and category:
            product_id = str(uuid.uuid4())
            data = image.read()
            print(product_id)
            sqlconnection = sqlite3.Connection(currentlocation + "/database/products.db")
            cursor = sqlconnection.cursor()
            query = "INSERT INTO product (productID, productname, description, sellerID, image, price, category) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (product_id, product_name, description, id, data, price, category))
            sqlconnection.commit()
            sqlconnection.close()
    return render_template('seller-create-listing.html' , id=id)

@app.route("/seller/yourlistings/<id>")
def sellerlistings(id):
    return render_template("seller-your-listings.html" , id=id)

@app.route("/login/<var>")
def home(var):
    type = var
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register/buyer", methods=["GET","POST"])
def register_buyer():
    if request.method == "POST":
        dUN = request.form['Demail_address']
        dPW = request.form['Dpassword']
        firstname = request.form['DFN']
        lastname = request.form['DLN']
        billaddress1 = request.form['Dba1']
        billaddress2 = request.form['Dba2']
        billaddress3 = request.form['Dba2']
        postcode = request.form['DPostC']
        cardnumber = request.form['Dcardnumber']
        cvcnumber = request.form['DCVC']
        expirerydate = request.form['Dexpirey']
        billname = request.form['Dbillname']
        print(dUN, postcode)
        sqlconnection = sqlite3.Connection(currentlocation + "/database/users.db")
        cursor = sqlconnection.cursor()
        query2 = f"INSERT INTO buyer VALUES('{dUN}', '{dPW}', '{firstname}', '{lastname}', '{billaddress1}', '{billaddress2}'," \
                 f" '{billaddress3}', '{postcode}', '{cardnumber}', '{cvcnumber}', '{expirerydate}', '{billname}' )"
        query3 = f"INSERT INTO catagories VALUES('{dUN}', 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5)"
        cursor.execute(query2)
        cursor.execute(query3)
        sqlconnection.commit()
        sqlconnection.close()
        return redirect("/")
    return render_template("buyerreg.html")


@app.route("/register/seller", methods=["GET","POST"])
def register_seller():
    if request.method == "POST":
        dUN = request.form['Semail_address']
        dPW = request.form['Spassword']
        firstname = request.form['SFN']
        lastname = request.form['SLN']
        sortcode = request.form['Ssortcode']
        accountnumber = request.form['Saccountnumber']
        cardnumber = request.form['Scardnumber']
        cvcnumber = request.form['SCVC']
        expirerydate = request.form['Sexpirey']
        billname = request.form['Sbillname']
        sqlconnection = sqlite3.Connection(currentlocation + "/database/users.db")
        cursor = sqlconnection.cursor()
        query2 = f"INSERT INTO seller VALUES('{dUN}', '{dPW}', '{firstname}', '{lastname}','{sortcode}' ,'{accountnumber}', '{cardnumber}', '{cvcnumber}', '{expirerydate}', '{billname}' )"
        cursor.execute(query2)
        sqlconnection.commit()
        return redirect("/")
    return render_template("sellerreg.html")


if __name__ == "__main__":
    app.run(debug=True)


def make_catagories(email):
    sqlconnection = sqlite3.Connection(currentlocation + "/database/users.db")
    cursor = sqlconnection.cursor()
    query = f"INSERT INTO seller VALUES('{email}', '20', '20', '20','20' ,'20')"
    cursor.execute(query)
    sqlconnection.commit()