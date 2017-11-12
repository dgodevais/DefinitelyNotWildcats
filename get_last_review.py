import pandas as pd
import csv
import json
import sys
import datetime as dt

# run on split business.json
biz_file = sys.argv[1]


def recent_review(biz_id, rev_df):
    date_list = []
    # loop to get dates of reviews for matching biz_id
    for i in range(len(rev_df)):
        if rev_df['business_id'][i] == biz_id:
            date_list.append(dt.datetime.strptime(rev_df['date'][i], '%Y-%m-%d').date())
    try:
        recent = max(date_list)
    except:
        recent = 'no review'
    return recent


# read in full business data
biz = []
with open(biz_file) as f:
    for line in f:
        biz.append(json.loads(line))

print('restaurant.json loaded')

# get all biz_ids
id_list = [i['business_id'] for i in biz]

# Make rev data a dataframe
with open('review.json') as f:
    rev_df = pd.DataFrame(json.loads(line) for line in f)

print('reviews.json loaded')

# for loop to write out biz_id + last review data
with open(str(biz_file + 'last_reviews.csv'), 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for biz_id in id_list:
        last_rev = recent_review(biz_id, rev_df)
        writer.writerow([biz_id] + [last_rev])
