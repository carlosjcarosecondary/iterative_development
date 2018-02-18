#################################################
# Configuration 
#################################################

# Importing the necessary libraries from SQLAlchemy 
# which will be useful when writing the mapping code
from sqlalchemy import Column, ForeignKey, Integer, String

# Importing the class that will allow the inheritance 
# of all the features of SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

# Importing the relationship to create our foreign key 
# relationships
from sqlalchemy.orm import relationship

# Importing the library to create our database
from sqlalchemy import create_engine

# Creating an instance of the declarative_base class
# that will show our classes as SQLAlchemy classes
Base = declarative_base()

#################################################
# Class
#################################################
class Restaurant(Base):

##################################
# Table
##################################
	__tablename__ = 'restaurant'

###################
# Mapper
###################
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)

	@property
	def serialize(self):
		return {
			'name': self.name
		}


#################################################
# Class
#################################################
class MenuItem(Base):

##################################
# Table
##################################
	__tablename__ = 'menu_item'

###################
# Mapper
###################
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)


######### Code to prepare data for JSON exchange #########
	@property
	def serialize(self):
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'price': self.price,
			'course': self.course,
		}


######### insert at end of file #########
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)

