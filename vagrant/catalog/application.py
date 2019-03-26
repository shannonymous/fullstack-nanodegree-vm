from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, SportCategory, SportItem

app = Flask(__name__)

engine = create_engine('sqlite:///sports.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Root
@app.route('/')
@app.route('/catalog/')
def catalog():
    categories = session.query(SportCategory).all()
    items = session.query(SportItem).order_by(SportItem.id.desc()).limit(10)
    latestItem = session.query(SportItem, SportCategory).outerjoin(SportCategory, SportCategory.id==SportItem.category_id).order_by(SportItem.id.desc()).limit(10)
    return render_template('catalog.html', categories=categories, items=items, latestItem = latestItem)
    #add login version of template

#Create routing for All items in a Sport category
@app.route('/catalog/<path:category_name>/Items')
def sport(category_name):
    currentcategory = session.query(SportCategory).filter_by(name = category_name).one()
    itemInCategory = session.query(SportItem).filter_by(category_id = currentcategory.id)
    categories = session.query(SportCategory).all()
    return render_template('sport.html', categories = categories, currentcategory = currentcategory, itemInCategory = itemInCategory)
    #add login version of template

#Create routing for specific item within Sport category
@app.route('/catalog/<path:category_name>/<path:item_name>')
def itemDescription(category_name, item_name):
    currentcategory = session.query(SportCategory).filter_by(name = category_name).one()
    item = session.query(SportItem).filter_by(category_id=currentcategory.id, name=item_name).one()
    return render_template('sportitem.html', item = item)

#Create routing for adding item to sport category
@app.route('/catalog/new', methods = ['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        newItem = SportItem( name=request.form['name'], description=request.form['description'], category_id = category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('sport', category_name = category_name))
    else:
        return render_template('newitem.html', categories = categories)

#Create routing for editing sport items
@app.route('/catalog/<path:category_name>/<path:item_name>/edit', methods = ['GET', 'POST'])
def editItem(category_name, item_name):
    currentcategory = session.query(SportCategory).filter_by(name = category_name).one()
    itemToEdit = session.query(SportItem).filter_by(category_id=currentcategory.id, name=item_name).one()
    if request.method == 'POST':
        itemToEdit.name = request.form['name']
        itemToEdit.description = request.form['description']
        itemToEdit.category = request.form['category']
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('itemDescription', category_name=category_name, item_name=item_name, i = itemToEdit))
    else:
        return render_template('editsportitem.html', i = itemToEdit)


#return render_template('sportitem.html', item = item)

#Create routing for deleting sport items
#@app.route('/catalog/<path:category_name>/<path:item_name>/delete', methods = ['GET', 'POST'])
#def deleteItem(category_name, item_name):

#Create login page

#hit up category JSON endpoint




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
