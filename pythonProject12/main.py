import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
query = "CREATE TABLE Product ("\
        "id STRING PRIMARY KEY,"\
        "image STRING NOT NULL)"
db = sqlite3.connect("database/product.db")
cursor = db.cursor()
cursor.execute(query)



