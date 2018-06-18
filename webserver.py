'''Filename: webserver.py'''

# Playthrough of the "Building a Server with HTTPBaseServer"
# tutorial with notes


from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import urllib

# My standard sqlalchemy imports
from sqlalchemy import create_engine # Make an engine for interacting with the SQLite DB
from sqlalchemy.orm import sessionmaker # Make a Object-Relational-Mapper session for the Engine
from database_setup import Base, Restaurant, MenuItem # Import my example DB Classes

from sqlalchemy import func

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()
# main, handler


substring_restaurant = lambda name: session.query(Restaurant).filter(func.lower(Restaurant.name).contains(func.lower(name))).all()

first_restaurant = lambda name: session.query(Restaurant).filter(func.lower(Restaurant.name).contains(func.lower(name))).first()

get_foods = lambda _restraunt: session.query(MenuItem).filter_by(restaurant = _restraunt).all()

def check_restaurant_name(user_input):
    """Returns whether or not user input is a Restaurant in our Database

    Parameters: User Input is a string

    Return: boolean: whether or not user_input is a Restaurant in our DB
    """
    results = substring_restaurant(user_input)
    return len(results) != 0

def list_restaurants(user_input):
    results = substring_restaurant(user_input)
    output = "<h1> Restaurants found: </h1>\n"
    for item in results:
        _name = item.name
        _address = urllib.parse.quote(item.name, safe='')
        output += '<p><a href="/restaurants/{address}">{name}</a></p>\n'.format(address = _address, name=_name)
    return output
        
STYLE_HTML_CSS = """
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
<style>

body {text-align:center;}
input[type="text"]
{
    width: 500px;
    border: 1px solid #CCC;
}
</style>
"""


def single_form(message):
    return """
<form method='POST' enctype='multipart/form-data' action='/hello'>
<input name="message" placeholder="{}" type="text">
<input type="submit" value="Submit">
</form>""".format(message)


def main():
    # Try to connect to localhost port 8080, using my own webserverHandler class
    try:

        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    # handle KeyboardInterrupt to be sure to close the socket so it doesn't get stuck open
    # when I try to close and rerun the program
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/index") or len(self.path.replace("/", "")) < 1:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><head>"
                output += STYLE_HTML_CSS
                output += "</head><body>"
                output += single_form("Enter a restaurant to see its menu") 
                output += "</body></html>"

                # In Python 3, we can't just write a string to HTTP.
                # This is because Python 3 has allowed for multiple different types of
                # Encodings to be transmitted. We need to specify one. We will choose utf-8
                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return
            if self.path.startswith("/restaurants"):
                path = self.path.split('/')
                if len(path) >= 3:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    restaurant = urllib.parse.unquote(path[2])
                    output = "<html><head>"
                    output += STYLE_HTML_CSS
                    output += "</head><body>"
                    output += "<h1>{name}</h1>".format(name=restaurant)
                    if not check_restaurant_name(restaurant):
                        output += "<p>Error: Restaurant Not Found</p>"
                    else:
                        restaurant = first_restaurant(restaurant)
                        foods = get_foods(restaurant)
                        for item in foods:
                            output += "<p>Item: {:20s}\tPrice: {:5s}</p>".format(item.name, item.price)
                    output += "<a href='/index'>Search Again</a>"
                    output += "</body></html>"
                    self.wfile.write(bytes(output, "utf-8"))
                    return
            raise Exception("File not found")
        except:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        #try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # getheader deprecated in python3. use get.
            #ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
            ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))
            

            #workaround for not being able to concat string to bytes in parse_multipart
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            else:
                raise Exception("Weird lookin' form")


            output = ""
            output += "<html><head>"
            output += STYLE_HTML_CSS
            output += "<body>"
            # messagecontent[0] is the utf-8 data. We want the string version of b'{Message}'
            # So we trim the first two and last characters.
            message = str(messagecontent[0])[2:-1]
            if check_restaurant_name(message):
                output += "<h1> %s: Restaurant Found!</h1>" % message
                output += list_restaurants(message)
            else:
                output += "<h1> %s: Not Found.</h1>" % message
            output += single_form("Enter A Restaurant to see its menu")
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))
            print(output)
        #except:
        #    print("ERROR")


if __name__ == '__main__':
    main()
