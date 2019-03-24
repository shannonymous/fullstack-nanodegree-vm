from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, SportCategory, SportItem

app = Flask(__name__)

engine = create_engine('sqlite:///sports.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog')
def catalog():
    categories = session.query(SportCategory).all()
    items = session.query(SportItem).order_by(SportItem.id.desc()).limit(10)
    latestItem = session.query(SportItem, SportCategory).outerjoin(SportCategory, SportCategory.id==SportItem.category_id).order_by(SportItem.id.desc()).limit(10)
    return render_template('catalog.html', categories=categories, items=items, latestItem = latestItem)
    #add login version of template

#Create routing for All items in a Sport category
@app.route('/catalog/<path:category_name>/Items')
def sport(category_name):
    categories = session.query(SportCategory).all()
    category = session.query(SportCategory).filter_by(name = category_name).one()
    itemInCategory = session.query(SportItem).filter_by(category_id = category.id).all()
    count = len(itemInCategory)
    return render_template('sport.html', categories = categories, category = category, itemInCategory = itemInCategory, count = count)
    #add login version of template

#Create routing for specific item within Sport category
#@app.route('/catalog/<path:category>/<path:name>')
#def sportitem(category, name):
#    return render_template('sportitem.html', catalog=catalog)

#Create routing for adding item to sport category

#Create routing for editing sport items

#Create routing for deleting sport items

#Create login page

#hit up category JSON endpoint




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
