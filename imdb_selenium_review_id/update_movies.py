# this script is for transferring data from one database to another

from db import Review, Movie
from db1 import Reviews, Movies
from dateutil.parser import parse
import re
from time import sleep
import pandas as pd
from datetime import datetime

exist_review = Review.select()
exist_movie = Movie.select()

"""
class Movie(Model):
    title_id = TextField()
    title = TextField()
    movie_type = TextField()
    duration = TextField()
    category = TextField()
    release = TextField()
    creaters = TextField()
    director = TextField()
    writer = TextField()
    stars = TextField()
    summary = TextField()
            
"""
query = Movie.select()
year = []
for q in query:
    print(q.release)
    try:
        release_date = re.findall('\d+\s\w+\s\d+',q.release)[0]
    except:
        release_date = None
    try:
        country = re.findall('\(([a-zA-Z]+)',q.release)[0]
    except:
        country = None
    try:
        years = re.findall('\((\d+.\d+)',q.release)
        year = years[0]
    except:
        year = None
        
    if not year:
        year = release_date
   
    
    if q.duration == '':
        duration = None
    else:
        duration = q.duration
        
    if q.category == '':
        category = None
    else:
        category = q.category
        
    if q.creaters == '':
        creaters = None
    else:
        creaters = q.creaters
        
    if q.director == '':
        director = None
    else:
        director = q.director
        
    if q.writer == '':
        writer = None
    else:
        writer = q.writer

    #Movies.insert_from(
    #       Movie.select(Movie.title_id, Movie.title, Movie.movie_type, Movie.stars, Movie.summary),
    #       fields=[Movies.title_id, Movies.title, Movies.movie_type, Movies.stars, Movies.summary])
    #   .execute()
    
    Movies.update(
           duration = duration, category= category, year=year, country=country, creaters=creaters, director= director,writer=writer
           ).where(Movies.title_id == q.title_id).execute()
       
    
    """
    query = Tweet.update(is_published=True).where(Tweet.creation_date < today)
>>> query.execute()  # Returns the number of rows that were updated.
"""
    
    print(year)