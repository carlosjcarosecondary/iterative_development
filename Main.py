'''
Created on Feb 13th, 2018

# 1. Routing --> Done
# 2. Templates & forms --> 
# 3. CRUD functionality
# 4. API end points

@author: carloscaro
'''
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def Restaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurant.html', restaurants = restaurants)

@app.route('/restaurants/new', methods = ['GET', 'POST'])
def NewRestaurant():
	if request.method == 'POST':
		if request.form['submit'] == 'Add':
			newRestaurant = Restaurant(name = request.form['name'])
			session.add(newRestaurant)
			session.commit()
			flash('New restaurant has been added successfully')
			return redirect(url_for('Restaurants'))
		elif request.form['submit'] == 'Cancel':
			return redirect(url_for('Restaurants'))
	else:
		return render_template('restaurant_new.html')

@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def EditRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['submit'] == 'Edit':
			editedRestaurant.name = request.form['name']
			session.add(editedRestaurant)
			session.commit()
			flash('Restaurant has been edited successfully')
			return redirect(url_for('Restaurants'))
		elif request.form['submit'] == 'Cancel':
			return redirect(url_for('Restaurants'))
	else:
		return render_template('restaurant_edit.html', restaurant_id = restaurant_id, 
			a = editedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def DeleteRestaurant(restaurant_id):
	deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['submit'] == 'Delete':
			session.delete(deletedRestaurant)
			session.commit()
			flash('Restaurant has been deleted successfully')
			return redirect(url_for('Restaurants'))
		elif request.form['submit'] == 'Cancel':
			return redirect(url_for('Restaurants'))
	else:
		return render_template('restaurant_delete.html', restaurant_id = restaurant_id, 
			a = deletedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/', methods = ['GET', 'POST'])
def RestaurantMenu(restaurant_id):
	menuRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return render_template('restaurant_menu.html', a = menuRestaurant, b = menuItems, 
		restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def RestaurantMenuNew(restaurant_id):
	menuRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	if request.method == 'POST':
		if request.form['submit'] == 'Add':
			newMenuItem = MenuItem(
				name = request.form['name'],
				description = request.form['description'],
				price = request.form['price'],
				restaurant_id = restaurant_id)
			session.add(newMenuItem)
			session.commit()
			flash('New menu item has been added successfully')
			# return render_template('restaurant_menu.html', restaurant_id = restaurant_id,
			# 	a = menuRestaurant, b = menuItems)
			return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
		elif request.form['submit'] == 'Cancel':
			return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('restaurant_menu_new.html', restaurant_id = restaurant_id, 
		a=menuRestaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def RestaurantMenuEdit(restaurant_id, menu_id):
	return 'Edit item in Restaurant Menu'

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def RestaurantMenuDelete(restaurant_id, menu_id):
	return 'Delete item in Restaurant Menu'

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 7777)