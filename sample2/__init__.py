from __future__ import division
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker
from table import *
engine = create_engine('sqlite:///data.db', echo=True)

app = Flask(__name__)

from app import app