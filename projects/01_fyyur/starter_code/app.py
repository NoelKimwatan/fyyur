#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from email.policy import default
import os
from os import environ
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime

from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app,db)




def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  #Query all the venues
  venues = Venue.query.all()
  data = list()

  states = list({venue.state for venue in venues})
  print("States")
  states_cities = {state:{venue.city for venue in Venue.query.filter(Venue.state == state).all()} for state in states}
  print("State cities",states_cities)

  data =list()

  for state in states:
    print("Print state",state)
    cities = states_cities[state]
    print("Cities in state",cities)
    for city in cities:
      print("Loop city")
      temp =dict()
      temp["state"] = state
      temp["city"] = city
      temp["venues"] = Venue.query.filter(Venue.state == state, Venue.city == city).all()
      data.append(temp)


  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  #Implemented a case insensitive search using ilike
  serch_term = "%{}%".format(request.form.get("search_term"))
  venues = Venue.query.filter(Venue.name.ilike(serch_term)).all()

  #Formated the search into the appropriate response format
  response = {
    "count":len(venues),
    "data":venues
    }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  #Query all venues
  venue = Venue.query.get(venue_id)
  
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  error = False
  new_venue = Venue(
      name = request.form.get("name"), 
      city = request.form.get("city"),
      state = request.form.get("state"),
      address = request.form.get("address"),
      phone = request.form.get("phone"),
      genres = request.form.get("genres"),
      facebook_link = request.form.get("facebook_link"),
      image_link = request.form.get("image_link"),
      website = request.form.get("website_link"),
      seeking_talent = True if request.form.get("seeking_talent") == 'y' else False,
      seeking_description = request.form.get("seeking_description")
  )

  print("Trying to add new venue")
  #Implementing the new venue insert with a try catch statement
  try:
    db.session.add(new_venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    print("DB session create failed")
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form.get("name") + ' could not be listed.')

  #Closing session
  db.session.close()


  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  print("Venue delete query entered")
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue = Venue.query.get(venue_id)
  venue_name = venue.name

  print("Trying to delete a record")
  db.session.delete(venue)
  db.session.commit()
  flash('Venue ' + venue_name + ' was deleted successfully!')

  try:
    print("Trying to delete a record")
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue_name + ' was deleted successfully!')
  except:
    print("delete uncesseful")
    db.session.rollback()
    flash('Venue ' + venue_name + ' deletion failed')
  
  db.session.close()

  #--------------------------------------------------------------------------------------
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  # Query data
  real_data = Artist.query.all()
  return render_template('pages/artists.html', artists=real_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  #Implementing a case insensitive search for artists
  serch_term = "%{}%".format(request.form.get("search_term"))
  artists = Artist.query.filter(Artist.name.ilike(serch_term)).all()

  #Formating the response into the appropriate format
  response ={
    "count":len(artists),
    "data":artists
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  #Quering all artists
  artist = Artist.query.get(artist_id)
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)


  # TODO: populate form with fields from artist with ID <artist_id> -->Done
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  #Editing artist
  edited_artist = Artist.query.get(artist_id)




  edited_artist.name = request.form.get("name") 
  edited_artist.city = request.form.get("city")
  edited_artist.state = request.form.get("state")
  edited_artist.phone = request.form.get("phone")
  edited_artist.genres = request.form.get("genres")
  edited_artist.facebook_link = request.form.get("facebook_link")
  edited_artist.image_link = request.form.get("image_link")
  edited_artist.website = request.form.get("website_link")
  edited_artist.seeking_venue = False if request.form.get("seeking_venue") == None else True
  edited_artist.seeking_description = request.form.get("seeking_description")

  print("Stored value",edited_artist.seeking_venue)



  try:
    print("Trying to edit artist details")
    db.session.add(edited_artist)
    db.session.commit()
    print("Edit successful")
    flash('Artist ' + request.form.get("name")  + ' successfully edited!')
  except:
    print("Edit Failed")
    db.session.rollback()
    flash('Artist ' + request.form.get("name")  + ' edit failed!')

  db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>  --->Done
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  print("Seeeking talent",request.form.get("seeking_talent"))
  edited_venue = Venue.query.get(venue_id)
  edited_venue.name = request.form.get("name")
  edited_venue.city = request.form.get("city")
  edited_venue.state = request.form.get("state")
  edited_venue.address = request.form.get("address")
  edited_venue.phone = request.form.get("phone")
  edited_venue.genres = request.form.get("genres")
  edited_venue.facebook_link = request.form.get("facebook_link")
  edited_venue.image_link = request.form.get("image_link")
  edited_venue.website = request.form.get("website_link")
  edited_venue.seeking_talent = True if request.form.get("seeking_talent") == 'on' else False
  edited_venue.seeking_description = request.form.get("seeking_description")

  try:
    db.session.add(edited_venue)
    db.session.commit()
  except:
    db.session.rollback()


  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  new_artist = Artist(
    name = request.form.get("name"), 
    city = request.form.get("city"),
    state = request.form.get("state"),
    phone = request.form.get("phone"),
    genres = request.form.get("genres"),
    facebook_link = request.form.get("facebook_link"),
    image_link = request.form.get("image_link"),
    website = request.form.get("website_link"),
    seeking_venue = False if request.form.get("seeking_venue") == None else True,
    seeking_description = request.form.get("seeking_description")
  )

  try:
    print("Tring to create an artist")
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + new_artist.name + ' could not be listed.')

  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  #Query all shows

  real_data = Show.query.all() 
  for data in real_data:
    print("Venue name",data.venue_name)
    print("Artist name",data.artist_name)
  return render_template('pages/shows.html', shows=real_data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  #Converting start time dat format into the appropriate format
  start_time = format_datetime(request.form.get("start_time"))


  new_show = Show(
    artist_id = request.form.get("artist_id"),
    venue_id = request.form.get("venue_id"),
    start_time = start_time
  )



  try:
    db.session.add(new_show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')

  db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
