import json
import datetime as dt
import csv
import os
from textblob import TextBlob
# from Queue import Queue
# from threading import Thread, RLock
from multiprocessing import Process, JoinableQueue as Queue
from itertools import chain, islice
import _strptime

strptime = dt.datetime.strptime

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

    def write_rating_dict_to_csv(ratings_dict, out_file_path, header=False):
        with open(out_file_path, 'a') as out_f:
            if header:
                out_f.write(
                    "biz_id,year,rating_sum,rating_count,polarity_sum,polarity_count,sentiment_sum,sentiment_count\n")
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
                    out_f.write(outline)

    def chunks(iterable, n):
        "chunks(ABCDE,2) => AB CD E"
        iterable = iter(iterable)
        while True:
            # store one line in memory,
            # chain it to an iterator on the rest of the chunk
            yield chain([next(iterable)], islice(iterable, n - 1))

    file_q = Queue(maxsize=0)
    files_splits = []
    chunk_size = 100000
    new_file_path = write_dir + '/' + os.path.basename(json_file_path)
    with open(json_file_path) as bigfile:
        for i, lines in enumerate(chunks(bigfile, chunk_size)):
            file_split = '{}.{}'.format(new_file_path, i)
            file_q.put(file_split)
            files_splits.append(file_split)
            with open(file_split, 'w') as f:
                f.writelines(lines)

    print "The following sub files were created: " + str(files_splits)

    def process_line(file_queue, out_file):
        while not file_queue.empty():
            fname = file_queue.get()
            ratings_dict = {}
            print "Starting thread for file {}".format(fname)
            with open(fname) as f:
                for line in f:
                    cur_rev = json.loads(line)
                    biz_id = cur_rev['business_id']
                    cur_rev_date = strptime(cur_rev['date'], '%Y-%m-%d').date()
                    cur_rev_year = cur_rev_date.year
                    if cur_rev_year in [2014, 2015, 2016]:
                        text_blob_vals = TextBlob(cur_rev['text'])
                        if biz_id not in ratings_dict:
                            ratings_dict[biz_id] = {cur_rev_year: {}}
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
            print "Done processing file thread for file {}".format(fname)
            write_rating_dict_to_csv(ratings_dict, out_file)
            print "Done writing file thread for file {}".format(out_file)
            file_queue.task_done()

    num_threads = 8
    workers = []
    thread_out_files = []
    for i in range(num_threads):
        out_file = csv_file_path + str(i)
        thread_out_files.append(out_file)
        worker = Process(target=process_line, args=(file_q, out_file,))
        worker.daemon = True
        worker.start()
        workers.append(worker)

    [x.join() for x in workers]

    for files_split in files_splits:
        os.remove(files_split)

    print "Threads are done! Combining dicts!"

    def combine_ratings_files(files):
        combined = {}
        for f_name in files:
            print "Combining file {}".format(f_name)
            with open(f_name) as f:
                first = True
                for line in f:
                    if first:
                        first = False
                    else:
                        fields = line.split(',')
                        biz_id = fields[0]
                        year = int(fields[1])
                        rating_sum = float(fields[2])
                        rating_count = float(fields[3])
                        polarity_sum = float(fields[4])
                        polarity_count = float(fields[5])
                        sentiment_sum = float(fields[6])
                        sentiment_count = float(fields[7])
                        if biz_id not in combined:
                            combined[biz_id] = {year: {}}
                        if year not in combined[biz_id]:
                            combined[biz_id][year] = {}
                        if 'rating_sum' not in combined[biz_id][year]:
                            combined[biz_id][year]['rating_sum'] = rating_sum
                            combined[biz_id][year]['rating_count'] = rating_count
                            combined[biz_id][year]['polarity_sum'] = polarity_sum
                            combined[biz_id][year]['polarity_count'] = polarity_count
                            combined[biz_id][year]['sentiment_sum'] = sentiment_sum
                            combined[biz_id][year]['sentiment_count'] = sentiment_count
                        else:
                            combined[biz_id][year]['rating_sum'] += rating_sum
                            combined[biz_id][year]['rating_count'] += rating_count
                            combined[biz_id][year]['polarity_sum'] += polarity_sum
                            combined[biz_id][year]['polarity_count'] += polarity_count
                            combined[biz_id][year]['sentiment_sum'] += sentiment_sum
                            combined[biz_id][year]['sentiment_count'] += sentiment_count
        return combined

    all_ratings = combine_ratings_files(thread_out_files)
    write_rating_dict_to_csv(all_ratings, csv_file_path, header=True)

    for thread_file in thread_out_files:
        os.remove(thread_file)
