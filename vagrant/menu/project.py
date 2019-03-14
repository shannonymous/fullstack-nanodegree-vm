from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, menuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Making an API Endpoint (GET request)
@app.route('/restaurants/<int:restaurant_id>/menu/json')
def restaurantMenuJSON(restaurant_id):
    resturant = session.query(Restaurant.filter_by(id = restaurant_id).one()
    items = session.query(menuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(menuItems=[i.serialize for i in items])


@app.route('/')
@app.route('/hello')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).filter_by(id = 5)
    output = ''
    for r in restaurants:
        output += r.name + '</br>'
        output += r.id +'</br>'
    return output



@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(menuItem).filter_by(restaurant_id = restaurant.id)
    #output = ''
    #for i in items:
    #    output += i.name + '</br>'
    #    output += i.description +'</br>'
    #    output += i.price + '</br></br>'
    #return output
    return render_template('menu.html', restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newMenuItem = menuItem( name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id = restaurant_id)
        session.add(newMenuItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
    #return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    itemToEdit = session.query(menuItem).filter_by(id = menu_id, restaurant_id = restaurant_id).one()
    if request.method == 'POST':
        itemToEdit.name = request.form['name']
        itemToEdit.description = request.form['description']
        itemToEdit.price = request.form['price']
        itemToEdit.course = request.form['course']
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, id = menu_id, i = itemToEdit)


    #return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete' methods = ['GET', 'POST'] )
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(return "page to delete a menu item. Task 3 complete!"



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
