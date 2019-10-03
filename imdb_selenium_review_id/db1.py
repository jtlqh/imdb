
from peewee import *
from configparser import ConfigParser
import time
#import sqlite3
#import psycopg2


# Initialize config parser
# ConfigParser will use % as a reference to another variable in your config file.
# If your password contains %, then you need to tell config parser don't interpolate it.
cfg = ConfigParser(interpolation=None)
cfg.read('conf.ini')

# Read the settings from config file using dictionary like notation
db_conf = cfg['database']
db_name = db_conf['db_name']
db_port = db_conf['db_port']
db_host = db_conf['db_host']
user = db_conf['user']
passwd = db_conf['passwd']

# Initialize a MySQL database connection
# Check more examples from the documentation: http://docs.peewee-orm.com/en/latest/peewee/quickstart.html
myDB = MySQLDatabase(db_name, host=db_host, port=int(db_port), user=user, passwd=passwd, charset='utf8mb4')
myDB.connect()

# The best way to understand how the Model and field works in peewee is to read the documentation
# http://peewee.readthedocs.io/en/latest/peewee/models.html#models-and-fields

# Initialize a class for the Review table


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

    class Meta:
        database = myDB


class Movies(Model):
    title_id = CharField(20, unique=True)
    title = TextField(null=True)
    movie_type = TextField(null=True)
    duration = TextField(null=True)
    category = TextField(null=True)
    year = TextField(null=True)
    country = TextField(null=True)
    creaters = TextField(null=True)
    director = TextField(null=True)
    writer = TextField(null=True)
    stars = TextField(null=True)
    summary = TextField(null=True)
            
    class Meta:
        database = myDB

# http://peewee.readthedocs.io/en/latest/peewee/api.html#Model.create_table
# safe (bool) – If set to True, the create table query will include an IF NOT EXISTS clause.
with myDB:
    Reviews.create_table(safe=True)
    #time.sleep(2)
    Movies.create_table(safe=True)
    #Review_summary.create_table(safe = True)


