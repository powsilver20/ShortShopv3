import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
connproducts = "database/products.db"
connusers = "database/users.db"
app = Flask(__name__)
productsdb = "CREATE TABLE product ("\
               "productID varchar(100) PRIMARY KEY, "\
               "productname varchar(30) NOT NULL, "\
               "description varchar(250) NOT NULL, " \
               "sellerID varchar(250) NOT NULL,"\
               "image BLOB NOT NULL, "\
               "price STRING NOT NULL, "\
               "category varchar(250) NOT NULL) "
sellerdatabase = "CREATE TABLE seller (" \
                 "email varchar(250) PRIMARY KEY UNIQUE, " \
                 "password varchar(30) NOT NULL , " \
                 "firstname varchar(250) NOT NULL, " \
                 "lastname varchar(250) NOT NULL, " \
                 "sortcode varchar(20) NOT NULL," \
                 "accountnumber varchar(20) NOT NULL," \
                 "cardnumber varchar(250) NOT NULL, " \
                 "cvcnumber INTEGER NOT NULL," \
                 "expirerydate varchar(250) NOT NULL," \
                 "billname varchar(250) NOT NULL)"
buyerdatabase ="CREATE TABLE buyer (" \
               "email varchar(250) PRIMARY KEY, " \
               "password varchar(30) NOT NULL UNIQUE, " \
               "firstname varchar(250) NOT NULL, " \
               "lastname varchar(250) NOT NULL, " \
               "billaddress1 varchar(250) NOT NULL, " \
               "billaddress2 varchar(250) NOT NULL, " \
               "billaddress3 varchar(250) NOT NULL, " \
               "postcode varchar(20) NOT NULL," \
               "cardnumber varchar(250) NOT NULL, " \
               "cvcnumber INTEGER NOT NULL," \
               "expirerydate varchar(250) NOT NULL," \
               "billname varchar(250) NOT NULL)"
catagories = "CREATE TABLE catagories ("\
               "userID varchar(230) PRIMARY KEY, "\
               "productive INTEGER NOT NULL, "\
               "fun INTEGER NOT NULL, "\
               "prank INTEGER NOT NULL, "\
               "health INTEGER NOT NULL, "\
               "fashion INTEGER NOT NULL," \
               "utilities INTEGER NOT NULL," \
               "comfort INTEGER NOT NULL," \
               "luxury INTEGER NOT NULL)"
drop = "DROP TABLE product"
db = sqlite3.connect(connproducts)
cursor = db.cursor()

cursor.execute(productsdb)
db.commit()
db.close()
# user = sqlite3.connect("database/users.db")
