import pandas as pd
import numpy as np
import json
import datetime as dt
import csv
from textblob import TextBlob

"""
Reads in review.json file and outputs a csv with following data by column:
'biz_id', 'total_counts', 'total_stars', 'total_rating',
 'last_year_counts', 'last_year_stars', 'last_year_rating',
 '
"""

rev_dict = {}

empty_year_dict = {'count':0, 
                   'stars':0, 
                   'text':'',  
                   'last_year_counts':0, 
                   'last_year_stars':0,
                   'last_year_text':'', 
                   'polarity':0.0, 
                   'sentiment':0.0, 
                   'last_year_polarity':0.0, 
                   'last_year_sentiment':0.0,}

year_starts = [dt.datetime.strptime("2017-01-01", '%Y-%m-%d').date(),
               dt.datetime.strptime("2016-01-01", '%Y-%m-%d').date(),
               dt.datetime.strptime("2015-01-01", '%Y-%m-%d').date(),
               dt.datetime.strptime("2014-01-01", '%Y-%m-%d').date()]

with open('review.json') as f:
    for line in f:
        cur_rev =  json.loads(line)
        biz_id = cur_rev['business_id']
        cur_rev_date = dt.datetime.strptime(cur_rev['date'], '%Y-%m-%d').date()
        # create empty dict
        if biz_id not in rev_dict:
                rev_dict[biz_id] = {}
                for cur_year in year_starts:
                    rev_dict[biz_id][str(cur_year.year)] = empty_year_dict.copy()
        # for each add count and stars
        for cur_year in year_starts:            
            if cur_rev_date.year < cur_year.year:
                rev_dict[biz_id][str(cur_year.year)]['count'] += 1
                rev_dict[biz_id][str(cur_year.year)]['stars'] += cur_rev['stars']
                rev_dict[biz_id][str(cur_year.year)]['text'] += cur_rev['text']
            if cur_rev_date.year == cur_year.year - 1:
                rev_dict[biz_id][str(cur_year.year)]['last_year_counts'] += 1
                rev_dict[biz_id][str(cur_year.year)]['last_year_stars'] += cur_rev['stars']
                rev_dict[biz_id][str(cur_year.year)]['last_year_text'] += cur_rev['text']
        
# Add scores              
for biz_id in rev_dict:
    for year in rev_dict[biz_id]:
        if rev_dict[biz_id][year]['last_year_counts'] != 0:
            rev_dict[biz_id][year]['tot_rating'] = rev_dict[biz_id][year]['stars'] / rev_dict[biz_id][year]['count']
        else:
            rev_dict[biz_id][year]['tot_rating'] = np.nan
        if rev_dict[biz_id][year]['last_year_counts'] != 0:
            rev_dict[biz_id][year]['last_year_rating'] = rev_dict[biz_id][year]['last_year_stars'] / rev_dict[biz_id][year]['last_year_counts']
        else:
            rev_dict[biz_id][year]['last_year_rating'] = np.nan
        if len(rev_dict[biz_id][year]['text']) != 0:
            rev_dict[biz_id][year]['polarity'] = TextBlob(rev_dict[biz_id][year]['text']).sentiment[0]
            rev_dict[biz_id][year]['sentiment'] = TextBlob(rev_dict[biz_id][year]['text']).sentiment[1]
        else:
            rev_dict[biz_id][year]['polarity'] = np.nan
            rev_dict[biz_id][year]['sentiment'] = np.nan
        if len(rev_dict[biz_id][year]['last_year_text']) != 0:
            rev_dict[biz_id][year]['last_year_polarity'] = TextBlob(rev_dict[biz_id][year]['text']).sentiment[0]
            rev_dict[biz_id][year]['last_year_sentiment'] = TextBlob(rev_dict[biz_id][year]['text']).sentiment[1]
        else:
            rev_dict[biz_id][year]['last_year_polarity'] = np.nan
            rev_dict[biz_id][year]['last_year_sentiment'] = np.nan
                
                
with open(str('yearly_reviews.csv'), 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['biz_id', 'total_counts', 'total_stars', 'total_rating',
                     'last_year_counts', 'last_year_stars', 'last_year_rating',
                    'polarity', 'sentiment', 'last_year_polarity', 'last_year_sentiment' ])
    for biz_id in rev_dict:
        for cur_year in year_starts:
            writer.writerow([str(biz_id), str(cur_year.year), str(rev_dict[biz_id][str(cur_year.year)]['count']), 
                str(rev_dict[biz_id][str(cur_year.year)]['stars']), 
                str(round(rev_dict[biz_id][str(cur_year.year)]['tot_rating'], 3)),
                str(rev_dict[biz_id][str(cur_year.year)]['last_year_counts']),
                str(rev_dict[biz_id][str(cur_year.year)]['last_year_stars']),
                str(round(rev_dict[biz_id][str(cur_year.year)]['last_year_rating'], 3)),
                str(round(rev_dict[biz_id][str(cur_year.year)]['polarity'], 3)),
                str(round(rev_dict[biz_id][str(cur_year.year)]['sentiment'], 3)),
                str(round(rev_dict[biz_id][str(cur_year.year)]['last_year_polarity'], 3)),
                str(round(rev_dict[biz_id][str(cur_year.year)]['last_year_sentiment'], 3))
                            ])

