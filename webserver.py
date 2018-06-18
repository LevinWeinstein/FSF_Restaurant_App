'''Filename: webserver.py'''

# Playthrough of the "Building a Server with HTTPBaseServer"
# tutorial with notes


from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import urllib


# A Constant dictionary for forms, with keys being which form I want,
# and values being a field name that I only use in that form.
FORMS = {"SEARCH_RESTAURANT":"message", "ADD_MENU_ITEM":"description"}

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
get_field_from = lambda string, fields: str(fields.get(string)[0])[2:-1]


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


body {
    text-align:center;
}

.deleter {
    display: inline-block;
}

input[type="text"]{
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

def delete_form(item):
    return """
<form class='deleter' method='POST' enctype='multipart/form-data' action='/delete_item'>
<input name="delete_item_name" type="hidden" value="{}">
<input name="delete_from_restaurant" type="hidden" value="{}">
<input type="submit" value="Delete">
""".format(item.name, item.restaurant.name)


def add_menu_item_form(_restaurant_name):
    _restaurant = first_restaurant(_restaurant_name)
    return """
<form method='POST' enctype='multipart/form-data' action='hello'>
<input name="name" placeholder="Name of Food" type="text">
<input name="price" placeholder="Price" type="text">
<input name="course" placeholder="Course" type="text">
<input name="restaurant" type="hidden" value="{}">
<input name="description" placeholder="Description" type="text">
<input type="submit" value="Submit">
""".format(_restaurant.name)

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

    def handle_restaurant_search_form_post(self, fields):   
        # messagecontent[0] is the utf-8 data. We want the string version of b'{Message}'
        # So we trim the first two and last characters.
        message = get_field_from('message', fields)
        output = "<html><head>"
        output += STYLE_HTML_CSS
        output += "<body>"
        if check_restaurant_name(message):
            output += "<h1>" + list_restaurants(message) + "</h1>"
        else:
            output += "<h1> Not Results Found for %s.</h1>" % message
        output += single_form("Enter A Restaurant to see its menu")
        output += "</body></html>"
        self.wfile.write(bytes(output, "utf-8"))
        print(output)
        return

    def handle_add_menu_item_form_post(self, fields):
        _name = get_field_from('name', fields)
        _price = get_field_from('price', fields) 
        restaurant_name = get_field_from('restaurant', fields)
        for i in range(100):
            print(restaurant_name)
        _description = get_field_from('description', fields)
        _course = get_field_from('course', fields)

        _restaurant = first_restaurant(restaurant_name)
        existing_food = session.query(MenuItem).filter_by(restaurant=_restaurant, name=_name).all()
        output = "<html><head>"
        output += STYLE_HTML_CSS
        output += "</head><body>"
        if len(existing_food):
            output += "<p>An item already exists with that exact spelling and spacing.</p>"
            output += "<p>Try a slightly different spelling if you want to add another item, or delete the first one<p>"

        else:
            new_food = MenuItem(name=_name, description=_description, price=_price, course=_course, restaurant=_restaurant)
            session.add(new_food)
            session.commit()
            output += "<p>Added {} to the menu at {}!".format(_name, _restaurant.name)
            output += "\n\n"
        output += "<a href='/index'>Search Again</a>"
        self.wfile.write(bytes(output, "utf-8"))
        print(output)
        return

    def handle_delete_item_form_post(self, fields):
        _name = get_field_from('delete_item_name', fields)
        _restaurant_name = get_field_from('delete_from_restaurant', fields)

        _restaurant = first_restaurant(_restaurant_name)

        output = "<html><head>"
        output += STYLE_HTML_CSS
        output += "</head><body>"
        try:
            _food = session.query(MenuItem).filter_by(restaurant=_restaurant, name=_name).first()
            "<p>Deleting {} from {}</p>".format(_food.name, _food.restaurant.name)
            session.delete(_food)
            session.commit()
        except:
            output += "<p>This item has already been deleted.</p>"
        output += "<a href='/index'>Search Again</a>"
        output += "</body></html>"
        self.wfile.write(bytes(output, "utf-8"))
        print(output)
        return
    
    def handle_index(self):
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

    def handle_restaurant_page(self):
        path = self.path.split('/')
        if len(path) >= 3 and len(path[-1]):
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
            elif len(path) == 4 and path[-1] == "add":
                output += "<p>Add A menu Item!</p>"
                output += add_menu_item_form(restaurant)
            else:
                restaurant = first_restaurant(restaurant)
                foods = get_foods(restaurant)
                for item in foods:
                    output += "<p>Item: {:20s}\tPrice: {:5s}".format(item.name, item.price) + delete_form(item) + "</p>"
                output += '<a href="{}/add">Add a menu item</a>   '.format(self.path)
            output += "<a href='/index'>Search Again</a>"
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))
        else:
            self.handle_index()

    def do_GET(self):
        try:
            if self.path.endswith("/index") or len(self.path.replace("/", "")) < 1:
                self.handle_index()
                return

            if self.path.startswith("/restaurants"):
                self.handle_restaurant_page()
                return
            raise Exception("File not found")
        except:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
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
                if 'message' in fields:
                     self.handle_restaurant_search_form_post(fields)
                     return
                elif 'price' in fields:
                    self.handle_add_menu_item_form_post(fields)
                    return
                elif 'delete_item_name' in fields:
                    self.handle_delete_item_form_post(fields)
                    return
            else:
                raise Exception("Weird lookin' form")

        except:
            print("ERROR")


if __name__ == '__main__':
    main()
