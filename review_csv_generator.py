import json
import datetime as dt
import csv
import os


def convert_reviews_json_file_to_csv(json_file_path, csv_file_path):
    """
    Writes the review.json file into a csv with first and last date for each business
    :param json_file_path: (str) path to the review.json file
    :param csv_file_path: (str) path to the new csv file
    :return:
    """
    write_dir = os.path.dirname(csv_file_path)
    if not os.path.isdir(write_dir):
        os.mkdir(write_dir)

    def get_last_review():
        rev_dict = {}
        with open(json_file_path) as f:
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
        return rev_dict

    with open(str(csv_file_path), 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        reviews = get_last_review()
        for biz_id, time_tuple in reviews.iteritems():
            writer.writerow([str(biz_id), str(time_tuple[0]), str(time_tuple[1])])
