import MySQLdb

username = 'benjihannam'
passwd = 'sas517785'
db_name = 'testing-for-player-welfare'
db_endpoint = 'testing-for-player-welfare.ctnijnxrr0tn.us-east-2.rds.amazonaws.com'
db = MySQLdb.connect(host=db_endpoint,  # your host 
                     user="benjihannam",       # username
                     passwd="sas517785",     # password
                     db=db_name)   # name of the database
 
# Create a Cursor object to execute queries.
cur = db.cursor()
 
# Select data from table using SQL query.
cur.execute("SELECT * FROM examples")
 
# print the first and second columns      
for row in cur.fetchall() :
    print row[0], " ", row[1]