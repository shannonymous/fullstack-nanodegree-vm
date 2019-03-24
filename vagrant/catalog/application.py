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

    return render_template('catalog.html', catalog=catalog)

#Create routing for All items in a Sport category
@app.route('/catalog/<path:category>/Items')
def sport(cateory)
    return render_template('sport.html', catalog=catalog)

#Create routing for specific item within Sport category
@app.route('/catalog/<path:category>/<path:name>')
def sportitem(category, name)
    return render_template('sportitem.html', catalog=catalog)

#Create routing for adding item to sport category

#Create routing for editing sport items

#Create routing for deleting sport items

#Create login page

#hit up category JSON endpoint




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
