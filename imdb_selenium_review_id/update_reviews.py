# this file is for tranferring data from one database to another

from db import Review, Movie
from db1 import Reviews, Movies
from dateutil.parser import parse
import re
from time import sleep
import pandas as pd
from datetime import datetime



"""
class Reviews(Model):
    title_id = TextField()
    review_id = CharField(20, unique=True)
    summary = TextField(null=True)
    content = TextField(null=True)
    username = TextField(null=True)
    date = DateTimeField(null=True)
    rating = TextField(null=True)
    scale = IntegerField(null=True)
    helpful_votes = IntegerField(null=True)
    total_votes = IntegerField(null=True)
            
"""

query = Review.select()
year = []

res = (Reviews
       .insert_from(
           Review.select(Review.title_id, Review.review_id, Review.summary, Review.content, Review.username, Review.date, \
                         None, Review.scale, Review.helpful_votes, Review.total_votes).where(Review.rating == ''),
           fields=[Reviews.title_id, Reviews.review_id, Reviews.summary, Reviews.content, Reviews.username, Reviews.date, \
                   Reviews.rating, Reviews.scale, Reviews.helpful_votes, Reviews.total_votes])
       
       .execute())
    

    
