'''Filename: SQLAlchemyNotes.py
   Author: Levin Weinstein   
'''

from sqlalchemy import create_engine # For creating an engine from a DB
from sqlalchemy.orm import sessionmaker # To begin a session from an engine
from database_setup import Base, Restaurant, MenuItem #Import my example DB Classes


from sqlalchemy import func # Important to check case insensitive matches
                            # usage:
                            #  user = models.User.query.filter(func.lower(User.username) == func.lower("LeViN"))


engine = create_engine('sqlite:///restaurantmenu.db') #create an engine from the database file
Base.metadata.bind = engine # bind our current database engine to the base class.
                            # This command just makes the connections between our class
                            # definitions, and their corresponding tables within our database

DBSession = sessionmaker(bind = engine)
session = DBSession()

#### NOTE: CREATE
myFirstRestaurant = Restaurant(name = "Pizza Palace") # Initialize an item representing a table
session.add(myFirstRestaurant) # add the new table to the session in the engine
session.commit()		# session.commit commits the changes in the actual database

restaurants = session.query(Restaurant).all() # Confirm additional restaurant by looking at the list of restaurants

cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)

print(len(session.query(MenuItem).filter_by(name="cheese pizza").all()))
session.add(cheesepizza)
session.commit()


## NOTE: DELETE [early attempt for the sake of cleanliness and curiousity]
##              [Real Version is Below]
# Before I added this loop, I had added a bunch of restaurants named Pizza Palace
# So I deleted them all. IMPORTANT TO NOTICE that it's near impossible to delete the objects
# with this item as a relationship once i've deleted this item and lost its handler.
# THEREFORE, it's important to delete it's relationships first before deleting it I think.
for item in restaurants:
    if item.name == "Pizza Palace":

        # this is the appropriate place to delete things that have this as a relationship
        # BEFORE I delete the restaurant itself
        foods = session.query(MenuItem).filter(MenuItem.restaurant == item).all()
        for food in foods:
            print("Deleting {} from {}".format(food.name, item.name))
            session.delete(food)
        
        print("Found pizza palace. Now deleting pizza palace")
        session.delete(item) # deletes a table
session.commit()

## NOTE: UPDATE
## Here's updating the price of all of the Veggie Burgers from all restaurants to $2.99
                                        # Also Noticed he's using filter_by, which seems
                                        # much more efficient
veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
for brgr in veggieBurgers:
    if brgr.price != '$2.99':
        brgr.price = '$2.99'
        session.add(brgr)
        session.commit()

for brgr in veggieBurgers:
    print(brgr.price)


## NOTE: DELETE
## (I already played with it before but this is the
## playthrough from the official tutorial)

try:
    spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
    print(spinach.restaurant.name, "has", spinach.name)
    session.delete(spinach)
    session.commit()
except:
    print("Spinach Ice Cream already deleted")



try:
    spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
    print("Somewhere else has Spinach Ice Cream too!")
except:
    pass
