import os
import pandas as pd
from db1 import Reviews
from dateutil.parser import parse

chunksize = 1000

os.chdir(r'C:\Users\jtlqh\bootcamp\my_projects\imdb\imdb_review\imdb_review\spiders')

#for reviews in pd.DataFrame(pd.read_csv('imdb_reviews.csv', chunksize=chunksize)):

for i,reviews in enumerate(pd.read_csv('imdb_reviews.csv',  chunksize=chunksize)):
    
    #continue
    if i<129:
        continue
    print(i)
    print(reviews.shape)
    #print(reviews.head())
    
    # save review date to sql database
    for idx in range(reviews.shape[0]):
        x= reviews.iloc[idx]
        #print(x.review_id)
        date = parse(x.date)
        if x.isnull().rating:
            rating = None
        else:
            rating = x.rating
            
        try:
            Reviews.update(summary=x.summary, content=x.content, username=x.username,\
                     date=date, rating=rating, scale=x.scale, helpful_votes=x.helpful_votes, total_votes=x.total_votes)\
                .where((Reviews.review_id == x.review_id) & (Reviews.summary.is_null()))\
                .execute()
        except: 
            try:
                content = ''.join([char if ord(char) < 128 else '' for char in x.content])
                summary = ''.join([char if ord(char) < 128 else '' for char in x.summary])
                Reviews.update(summary=summary, content=content, username=x.username,\
                         date=date, rating=rating, scale=x.scale, helpful_votes=x.helpful_votes, total_votes=x.total_votes)\
                    .where((Reviews.review_id == x.review_id) & (Reviews.summary.is_null()))\
                    .execute()
            except:
                continue