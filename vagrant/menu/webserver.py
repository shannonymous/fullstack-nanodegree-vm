from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#import CRUD Operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, menuItem

#creates session variable and connect to the DB
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                output += "<h1><a href=/restaurants/new>Make a new restaurant here</a></h1></br></br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='#'>Edit</a>"
                    output += "</br>"
                    output += "<a href='#'>Delete</a>"
                    #delete = session.query(Restaurant).filter_by(name = 'n').one()
                    #session.delete(spinach)
                    #session.commit()
                    output += "</br>"
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            #adding restaurants
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                #output += "Hello"
                output += "<h2>Add a restaurant to the database:<h2>"
                output += "<form method ='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='addRestaurantName' type='text' placeholder = 'New Restaurant Name'>"
                output += "<input type='submit' value='Create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            #hello
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello"
                output += "<form method ='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?<h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            #hola
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161;Hola! <a href ='/hello'>Back to Hello</a>"
                output += "<form method ='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?<h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('addRestaurantName')

                #Create new Restaurant class
                addRestaurant = Restaurant(name = messagecontent[0])
                session.add(addRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()



            #self.send_response(301)
            #self.end_headers()

            #ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            #if ctype == 'multipart/form-data':
            #    fields=cgi.parse_multipart(self.rfile, pdict)
            #    messagecontent = fields.get('message')

            #output = ""
            #output += "<html><body>"
            #output += "<h2>Okay, how about this:</h2>"
            #output += "<h1> %s <h1>" % messagecontent[0]

            #output += "<form method ='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?<h2><input name='addRestaurantName' type='text'><input type='submit' value='Submit'></form>"
            #output += "</body></html>"
            #self.wfile.write(output)
            #print output

            #for restaurant db


            output = ""
            output += "<html><body>"
            #output += "<h2>Okay, how about this:</h2>"
            #output += "<h1> %s <h1>" % messagecontent[0]

            output += "<form method ='POST' enctype='multipart/form-data' action='/restaurants'><h2>Add a new restaurant to the database:<h2><input name='addRestaurantName' type='text'><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output

        except:
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()




    except KeyboardInterrupt:
        print " entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
