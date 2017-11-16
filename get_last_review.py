import pandas as pd
import numpy as np
import json
import datetime as dt
import csv

# only read in the review.json
# hold on to first and last dates
rev_dict = {}
with open('review.json') as f:
    for line in f:
        cur_rev = json.loads(line)
        biz_id = cur_rev['business_id']
        cur_rev_date = dt.datetime.strptime(cur_rev['date'], '%Y-%m-%d').date()
        if biz_id in rev_dict:
            if rev_dict[biz_id][0] > cur_rev_date:
                rev_dict[biz_id][0] = cur_rev_date
            elif rev_dict[biz_id][1] < cur_rev_date:
                rev_dict[biz_id][1] = cur_rev_date
        else:
            rev_dict[biz_id] = [cur_rev_date, cur_rev_date]
            
with open(str('last_reviews.csv'), 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for key in rev_dict:
        writer.writerow([str(key), str(rev_dict[key][0]), str(rev_dict[key][1])])  
