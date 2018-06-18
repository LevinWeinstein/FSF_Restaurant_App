'''Filename: SQLAlchemyNotes.py
   Author: Levin Weinstein   
'''

from sqlalchemy import create_engine # For creating an engine from a DB
from sqlalchemy.orm import sessionmaker # To begin a session from an engine
from database_setup import Base, Restaurant, MenuItem #Import my example DB Classes

engine = create_engine('sqlite:///restaurantmenu.db') #create an engine from the database file
Base.metadata.bind = engine # bind our current database engine to the base class.
                            # This command just makes the connections between our class
                            # definitions, and their corresponding tables within our database

DBSession = sessionmaker(bind = engine)
session = DBSession()

#### Notes: CREATE
myFirstRestaurant = Restaurant(name = "Pizza Palace") # Initialize an item representing a table
session.add(myFirstRestaurant) # add the new table to the session in the engine
session.commit()		# session.commit commits the changes in the actual database

restaurants = session.query(Restaurant).all() # Confirm additional restaurant by looking at the list of restaurants

cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)

session.add(cheesepizza)
session.commit()


## DELETING


# Before I added this loop, I had added a bunch of restaurants named Pizza Palace
# So I deleted them all. IMPORTANT TO NOTE that it's near impossible to delete the objects
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

## UPDATING
session.commit() 
