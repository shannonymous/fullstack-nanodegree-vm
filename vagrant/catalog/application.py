from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, menuItem

app = Flask(__name__)

engine = create_engine('sqlite:///sports.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog')
def catalog():
    catalog =session.query(SportCategory).all()
    
    return render_template('sports.html', catalog=catalog)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
