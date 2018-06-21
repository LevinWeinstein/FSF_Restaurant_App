""" Filename: create_db.py
    Author  : Levin Weinstein
    Purpose : Create the initial database for the Restaurant Project
"""

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True) 
    name = Column(String(250), nullable=False)

class MenuItem(Base):
    __tablename__ = 'menu_item'
    
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

############  insert at end of file #############


# Textbook example of why if __name__ == '__main__':
# is important. At first when i used this file to
# create the DB, i forgot to put if __name__ == '__main__'
# here, then, whenever I ran my code, even though I'd moved
# my database elsewhere, it was initializing a new empty
# restaurantmenu.db in whichever folder I was working in.
if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.create_all(engine)
