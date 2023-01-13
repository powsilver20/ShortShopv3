import base64
import random

from flask import Flask, request, render_template, redirect
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





def Like(id, category):
    sqlconnection = sqlite3.Connection(currentlocation + "/database/users.db")
    cursor = sqlconnection.cursor()

    query = f"SELECT * From catagories WHERE userID = '{id}'"
    cursor.execute(query)
    rows = cursor.fetchall()

    sqlconnection.commit()
    cursor.close()
    sqlconnection.close()

    prodselect = random.randint(0,(len(rows))-1)
    rows= rows[prodselect]
    rows = list(rows)
    if category == "productive":
        i = 1
        q = "fun , prank , health, fashion, utilities, comfort, luxury"

    if category == "fun":
        i = 2
        q = "productive , prank , health, fashion, utilities, comfort, luxury"
    if category == "prank":
        i = 3
        q = "productive, fun, health, fashion, utilities, comfort, luxury"
    if category == "health":
        i = 4
        q = "productive, fun , prank, fashion, utilities, comfort, luxury"
    if category == "fashion":
        i = 5
        q = "productive, fun , prank , health, utilities, comfort, luxury"
    if category == "utilities":
        i = 6
        q = "productive, fun , prank , health, fashion, comfort, luxury"
    if category == "comfort":
        i = 7
        q = "productive, fun , prank , health, fashion, utilities, luxury"
    if category == "luxury":
        i = 8
        q = "productive, fun , prank , health, fashion, utilities, comfort"

    rows[i] = rows[i] * 1.1
    remainder = rows[i] * 0.1
    sub = remainder / len(rows)
    sqlconnection = sqlite3.Connection(currentlocation + "/database/users.db")
    cursor = sqlconnection.cursor()
    query2 = f"SELECT {q} From catagories WHERE userID = '{id}'"
    rows2 = cursor.execute(query2)
    sqlconnection.commit()
    cursor.close()
    sqlconnection.close()
    for z in range(1, (len(rows))):
        if z == i:
            continue
        rows[z] = rows[z] - sub

    sqlconnection = sqlite3.Connection(currentlocation + "/database/users.db")
    cursor = sqlconnection.cursor()
    query3 = f"UPDATE catagories SET productive = {rows[1]}, fun = {rows[2]}, prank = {rows[3]}, health = {rows[4]}, fashion = {rows[5]}, utilities = {rows[6]}, comfort = {rows[7]}, luxury = {rows[8]} WHERE userID = '{id}'"
    cursor.execute(query3)
    sqlconnection.commit()
    cursor.close()
    sqlconnection.close()

@app.route('/buyer/feed/<id>/<product>')
def feedpage(id, product):
    rand = random.uniform(0, 100)
    sqlconnection = sqlite3.Connection(currentlocation + "/database/users.db")
    cursor = sqlconnection.cursor()
    query = f"SELECT * From catagories WHERE userID = '{id}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    sqlconnection.commit()
    cursor.close()
    sqlconnection.close()
    rows = rows[0]
    select = ""
    p1 = rows[1]
    p2 = rows[1] + rows[2]
    p3 = rows[1] + rows[2] + rows[3]
    p4 = rows[1] + rows[2] + rows[3] + rows[4]
    p5 = rows[1] + rows[2] + rows[3] + rows[4] + rows[5]
    p6 = rows[1] + rows[2] + rows[3] + rows[4] + rows[5] + rows[6]
    p7 = rows[1] + rows[2] + rows[3] + rows[4] + rows[5] + rows[6] + rows[7]
    p8 = rows[1] + rows[2] + rows[3] + rows[4] + rows[5] + rows[6] + rows[7] + rows[8]

    if 0 <= rand < p1:
        select = "productive"
    if p1 <= rand < p2:
        select = "fun"
    if p2 <= rand < p3:
        select = "prank"
    if p3 <= rand < p4:
        select = "health"
    if p4 <= rand < p5:
        select = "fashion"
    if p5 <= rand < p6:
        select = "utilities"
    if p6 <= rand < p7:
        select = "comfort"
    if p7 <= rand <= p8:
        select = "luxury"
    print(select)

    sqlconnection = sqlite3.Connection(currentlocation + "/database/products.db")
    cursor = sqlconnection.cursor()
    query4 = f"SELECT * From product WHERE category = '{select}'"
    cursor.execute(query4)
    rows3 = cursor.fetchall()
    sqlconnection.commit()
    cursor.close()
    sqlconnection.close()
    print(len(rows3))
    prodselect = random.randint(0, (len(rows3)))
    if prodselect < 1:
        return render_template("feed.html", rows = ["","","","","","",""])

    rows3 = rows3[prodselect]
    rows3 = list(rows3)
    return render_template("feed.html",rows3)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/login/<type>", methods=["POST"])
def checklogin(type):
    UN = request.form['email_address']
    PW = request.form['password']
    sqlconnection = sqlite3.Connection(currentlocation + "/database/users.db")
    cursor = sqlconnection.cursor()

    query1 = f"SELECT * From {type} WHERE email = '{UN}' AND password = '{PW}'"
    cursor.execute(query1)
    rows = cursor.fetchall()
    if (len(rows)) == 1 and (type == "buyer"):
        return redirect(f"/buyer/feed/{UN}/x")

    if (len(rows)) == 1 and (type == "seller"):
        return redirect(f"/seller/home/{UN}")
        return render_template("seller-create-listing.html")

    else:
        return redirect(f"/login/{type}")


@app.route("/seller/home/<id>", methods=['POST', 'GET'])
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
            data = base64.b64encode(data).decode()
            print(product_id)
            sqlconnection = sqlite3.Connection(currentlocation + "/database/products.db")
            cursor = sqlconnection.cursor()
            query = "INSERT INTO product (productID, productname, description, sellerID, image, price, category) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (product_id, product_name, description, id, data, price, category))
            sqlconnection.commit()
            sqlconnection.close()
    return render_template('seller-create-listing.html', id=id)


@app.route("/seller/yourlistings/<id>")
def sellerlistings(id):
    print("pass")
    sqlconnection = sqlite3.Connection(currentlocation + "/database/products.db")
    cursor = sqlconnection.cursor()
    query = f"SELECT * FROM product WHERE sellerID = ?"
    cursor.execute(query, (id,))
    rows = cursor.fetchall()
    sqlconnection.commit()
    cursor.close()
    sqlconnection.close()

    return render_template("seller-your-listings.html", id=id, rows=rows, )


@app.route("/login/<var>")
def home(var):
    type = var
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register/buyer", methods=["GET", "POST"])
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


@app.route("/register/seller", methods=["GET", "POST"])
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


