"""Import flask"""

from flask import Flask
"""To import sqlalchemy"""

from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CSRFProtect
"""Instantiate Flask Object"""

app = Flask(__name__,instance_relative_config=True)



"""Import Config"""

app.config.from_pyfile('config.py')

db=SQLAlchemy(app)
csrf = CSRFProtect(app)
"""Importing routes"""
from pkg import mymodels
from pkg.myroutes import admin_route,user_route