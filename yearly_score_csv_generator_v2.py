import json
import datetime as dt
import csv
import os
from textblob import TextBlob
from Queue import Queue
from threading import Thread


def convert_reviews_json_file_to_rating_sentiment_csv(json_file_path, csv_file_path):
    """
    Returns a row for each year a business has been open with an aggregate rating and sentiment
    :param json_file_path: (str) path to the review.json file
    :param csv_file_path: (str) path to the new csv file
    :return:
    """
    write_dir = os.path.dirname(csv_file_path)
    if not os.path.isdir(write_dir):
        os.mkdir(write_dir)

    # q = Queue(maxsize=0)
    # num_threads = 10
    #
    # for i in range(num_threads):
    #     worker = Thread(target=do_stuff, args=(q,))
    #     worker.setDaemon(True)
    #     worker.start()

    ratings_dict = {}
    i = 0
    with open(json_file_path) as f:
        for line in f:
            cur_rev = json.loads(line)
            biz_id = cur_rev['business_id']
            cur_rev_date = dt.datetime.strptime(cur_rev['date'], '%Y-%m-%d').date()
            cur_rev_year = cur_rev_date.year
            if cur_rev_year in [2014, 2015, 2016]:
                text_blob_vals = TextBlob(cur_rev['text'])
                if biz_id not in ratings_dict:
                    ratings_dict[biz_id] = {cur_rev_year : {}}
                if cur_rev_year not in ratings_dict[biz_id]:
                    ratings_dict[biz_id][cur_rev_year] = {}
                if 'rating_sum' not in ratings_dict[biz_id][cur_rev_year]:
                    ratings_dict[biz_id][cur_rev_year]['rating_sum'] = float(cur_rev['stars'])
                    ratings_dict[biz_id][cur_rev_year]['rating_count'] = 1
                    ratings_dict[biz_id][cur_rev_year]['polarity_sum'] = float(text_blob_vals.sentiment[0])
                    ratings_dict[biz_id][cur_rev_year]['polarity_count'] = 1
                    ratings_dict[biz_id][cur_rev_year]['sentiment_sum'] = float(text_blob_vals.sentiment[1])
                    ratings_dict[biz_id][cur_rev_year]['sentiment_count'] = 1
                else:
                    ratings_dict[biz_id][cur_rev_year]['rating_sum'] += float(cur_rev['stars'])
                    ratings_dict[biz_id][cur_rev_year]['rating_count'] += 1
                    ratings_dict[biz_id][cur_rev_year]['polarity_sum'] += float(text_blob_vals.sentiment[0])
                    ratings_dict[biz_id][cur_rev_year]['polarity_count'] += 1
                    ratings_dict[biz_id][cur_rev_year]['sentiment_sum'] += float(text_blob_vals.sentiment[1])
                    ratings_dict[biz_id][cur_rev_year]['sentiment_count'] += 1
            # i += 1
            # if i == 50000:
            #     break

    with open(csv_file_path, 'w') as outfile:
        outfile.write("biz_id,year,rating_sum,rating_count,polarity_sum,polarity_count,sentiment_sum,sentiment_count\n")
        for biz_id, years in ratings_dict.iteritems():
            for year, stats in years.iteritems():
                outline = "{biz_id},{year},{rating_sum},{rating_count},{polarity_sum},{polarity_count}," \
                          "{sentiment_sum},{sentiment_count}\n".format(
                    biz_id=biz_id,
                    year=year,
                    rating_sum=stats['rating_sum'],
                    rating_count=stats['rating_count'],
                    polarity_sum=stats['polarity_sum'],
                    polarity_count=stats['polarity_count'],
                    sentiment_sum=stats['sentiment_sum'],
                    sentiment_count=stats['sentiment_count']
                )
                outfile.write(outline)
