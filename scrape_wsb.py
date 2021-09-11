from psaw import PushshiftAPI
import datetime
import psycopg2, config
from psycopg2 import extras

connection = psycopg2.connect(host=config.DB_LOCAL_HOST, 
                                database=config.DB_LOCAL_NAME, 
                                user=config.DB_LOCAL_USER, 
                                password=config.DB_LOCAL_PASSWORD)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# pulls data from stock table
cursor.execute("""SELECT * FROM stock""")
rows = cursor.fetchall()

# creates stock dictionary from data pulled from table 'stock'
stocks = {}
for row in rows:
    stocks['$' + row['symbol']] = row['id']
print(stocks)

api = PushshiftAPI()

start_time = int(datetime.datetime(2021, 9, 7).timestamp())

submissions = api.search_submissions(after=start_time,
                            subreddit='wallstreetbets',
                            filter=['url', 'author', 'title', 'subreddit'])

for submission in submissions:
    words = submission.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))

    if len(cashtags) > 0:
        #print(cashtags)
        #print(submission.created_utc)
        #print(submission.title)
        #print(submission.url)
        #print(submission.author)
        

        for cashtag in cashtags:
            submission_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat() #changing timestamp from unix
            
            try:
                cursor.execute("""INSERT INTO ticker_match (dt, stock_id, message, source, username, url)
                                VALUES (%s, %s, %s, 'wallstreetbets',%s, %s)
                            """,(submission_time, stocks[cashtag], submission.title, submission.author, submission.url))
                
                connection.commit()
            except Exception as e:
                print(e)
                connection.rollback()