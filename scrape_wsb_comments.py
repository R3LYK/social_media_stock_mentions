import pandas as pd
import datetime
from pmaw import PushshiftAPI

api = PushshiftAPI()

# must be in epoch time for pmaw
before = int(datetime.datetime(2021,9,9,0,0).timestamp())
after = int(datetime.datetime(2021,8,1,0,0).timestamp())
subreddit="wallstreetbets"
limit=100

comments = api.search_comments(subreddit=subreddit, 
                                    limit=limit, 
                                    before=before, 
                                    after=after)

for comment in comments:
    print(f'Retrieved {len(comments)} comments from Reddit')
    comments_df = pd.DataFrame(comments)
    #preview
    comments_df.head(5)
    comments_df.to_csv('./wsb_comments.csv', header=True, index=False, columns=list(comments_df.axes[1]))