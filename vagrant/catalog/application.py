from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, SportCategory, SportItem, User

from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Sports Catalog"

app = Flask(__name__)

engine = create_engine('sqlite:///sportswithusers.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#===================
# Login Routing
#===================

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    #return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

     # See if a user exists, if it doesn't make a new one

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User's Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('catalog'))

    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#===================
#  Routing
#===================
#Add JSON API to return all users
@app.route('/users.json')
def usersJSON():
    users = session.query(User).all()
    return jsonify(Users = [u.serialize for u in users])

#Add JSON API Endpoint
@app.route('/catalog.JSON')
@app.route('/catalog.json')
def catalogJSON():
    categories = session.query(SportCategory).all()
    items = session.query(SportItem).order_by(SportItem.id.desc()).limit(10)
    return  jsonify(SportCategories=[c.serialize for c in categories], SportLatestItems=[i.serialize for i in items])


#Root
@app.route('/')
@app.route('/catalog/')
def catalog():
    categories = session.query(SportCategory).all()
    items = session.query(SportItem).order_by(SportItem.id.desc()).limit(10)
    latestItem = session.query(SportItem, SportCategory).outerjoin(SportCategory, SportCategory.id==SportItem.category_id).order_by(SportItem.id.desc()).limit(10)
    return render_template('catalog.html', categories=categories, items=items, latestItem = latestItem, login_session=session)

#Create routing for All items in a Sport category
@app.route('/catalog/<path:category_name>/Items')
def sport(category_name):
    currentcategory = session.query(SportCategory).filter_by(name = category_name).one()
    itemsincategory = session.query(SportItem).filter_by(category_id = currentcategory.id)
    categories = session.query(SportCategory).all()
    return render_template('sport.html', categories = categories, currentcategory = currentcategory, itemsincategory = itemsincategory)
    #add login version of template

# Add endpoint for all items in category
@app.route('/catalog/<path:category_name>/items.json')
@app.route('/catalog/<path:category_name>/items.JSON')
def itemsJSON(category_name):
    currentcategory = session.query(SportCategory).filter_by(name=category_name).one()
    itemsincategory = session.query(SportItem).filter_by(category_id = currentcategory.id).all()
    return jsonify(Items = [i.serialize for i in itemsincategory])

#Create routing for specific item within Sport category
@app.route('/catalog/<path:category_name>/<path:item_name>')
def itemDescription(category_name, item_name):
    currentcategory = session.query(SportCategory).filter_by(name = category_name).one()
    item = session.query(SportItem).filter_by(category_id=currentcategory.id, name=item_name).first()
    return render_template('sportitem.html', item=item, category=currentcategory, login_session=session)


#Add JSON API Endpoint for specific item in category
@app.route('/catalog/<path:category_name>/<path:item_name>.JSON')
@app.route('/catalog/<path:category_name>/<path:item_name>.json')
def itemJSON(category_name, item_name):
    currentcategory = session.query(SportCategory).filter_by(name = category_name).one()
    item = session.query(SportItem).filter_by(category_id=currentcategory.id, name=item_name).first()
    return jsonify(Item=item.serialize)

#Create routing for adding item to sport category
@app.route('/catalog/newitem', methods = ['GET', 'POST'])
def newItem():
    categories = session.query(SportCategory).all()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = SportItem( name=request.form['name'], description=request.form['description'], category_id=request.form['category'], user_id=login_session['user_id'])
        session.add(newItem)
        #flash)('New item %s successfully created' %newItem.name)
        session.commit()
        return redirect(url_for('catalog'))
    else:
        return render_template('newitem.html', categories = categories)

#Create routing for editing sport items
@app.route('/catalog/<path:category_name>/<path:item_name>/edit', methods = ['GET', 'POST'])
def editItem(category_name, item_name):
    categories = session.query(SportCategory).all()
    currentcategory = session.query(SportCategory).filter_by(name = category_name).one()
    itemToEdit = session.query(SportItem).filter_by(category_id=currentcategory.id, name=item_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        itemToEdit.name = request.form['name']
        itemToEdit.description = request.form['description']
        itemToEdit.category = request.form['category']
        #itemToEdit.user = request.form
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('itemDescription', category_name=category_name, item_name=item_name, i = itemToEdit))
    else:
        return render_template('editsportitem.html', i = itemToEdit, categories=categories, currentcategory=currentcategory)


#Create routing for deleting sport items
@app.route('/catalog/<path:category_name>/<path:item_name>/delete', methods = ['GET','POST'])
def deleteItem(category_name, item_name):
    currentcategory = session.query(SportCategory).filter_by(name = category_name).one()
    currentitem = session.query(SportItem).filter_by(name=item_name, category_id=currentcategory.id).first()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
            session.delete(currentitem)
            session.commit()
            return redirect(url_for('catalog'))
    else:
            return render_template('deletesportitem.htmnl', currentitem = currentitem, currentcategory=currentcategory)

#Create routing for adding sports
@app.route('/catalog/new', methods = ['GET', 'POST'])
def newSport():
    categories = session.query(SportCategory).all()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newSport = SportCategory( name=request.form['name'] )
        session.add(newSport)
        session.commit()
        return redirect(url_for('catalog'))
    else:
        return render_template('newcategory.html', categories = categories)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
