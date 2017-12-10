import time

from businesses_csv_generator import convert_business_json_file_to_csv
from review_csv_generator import convert_reviews_json_file_to_first_last_csv
from tip_csv_generator import convert_tip_json_file_to_csv
from checkin_csv_generator import convert_checkins_json_file_to_csv
from yearly_score_csv_generator_v2 import convert_reviews_json_file_to_rating_sentiment_csv


def main():
    print "Starting the yelp data formatter process"

    data_dir = '../yelp-data/yelp_dir/'
    out_dir = '../yelp-data/formatted/'

    start_time = time.time()
    # convert_business_json_file_to_csv(data_dir + 'business.json', out_dir + 'business.csv')
    # print "Finished converting the businesses json file to csv."
    # print "Businesses conversion took {} seconds".format((time.time() - start_time))

    # review_start_time = time.time()
    # convert_reviews_json_file_to_first_last_csv(data_dir + 'review.json', out_dir + 'review_first_last.csv')
    # print "Finished converting the reviews json file to first and last csv."
    # print "First and last reviews conversion took {} seconds".format((time.time() - review_start_time))

    rating_start_time = time.time()
    convert_reviews_json_file_to_rating_sentiment_csv(data_dir + 'review.json', out_dir + 'ratings.csv')
    print "Finished converting the reviews json file to Ratings and Sentiment csv."
    print "Ratings and Sentiment conversion took {} seconds".format((time.time() - rating_start_time))
    #
    # tip_start_time = time.time()
    # convert_tip_json_file_to_csv(data_dir + 'tip.json', out_dir + 'tip.csv')
    # print "Finished converting the tips json file to csv."
    # print "Tips conversion took {} seconds".format((time.time() - tip_start_time))
    #
    # checkin_start_time = time.time()
    # convert_checkins_json_file_to_csv(data_dir + 'checkin.json', out_dir + 'checkin.csv')
    # print "Finished converting the checkin json file to csv."
    # print "Checkin conversion took {} seconds".format((time.time() - checkin_start_time))

    print "Yelp data formatter process complete!"
    print "Yelp data formatter took {} seconds".format((time.time() - start_time))


if __name__ == "__main__":
    main()
