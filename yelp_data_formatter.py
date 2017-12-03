import time

from businesses_csv_generator import convert_business_json_file_to_csv
from review_csv_generator import convert_reviews_json_file_to_csv
from tip_csv_generator import convert_tip_json_file_to_csv
from checkin_csv_generator import convert_checkins_json_file_to_csv


def main():
    print "Starting the yelp data formatter process"

    start_time = time.time()
    convert_business_json_file_to_csv('../yelp-data/yelp_dir/business.json', '../yelp-data/formatted/business.csv')
    print "Finished converting the businesses json file to csv."
    print "Businesses conversion took {} seconds".format((time.time() - start_time))

    review_start_time = time.time()
    convert_reviews_json_file_to_csv('../yelp-data/yelp_dir/review.json', '../yelp-data/formatted/review.csv')
    print "Finished converting the reviews json file to csv."
    print "Reviews conversion took {} seconds".format((time.time() - review_start_time))

    tip_start_time = time.time()
    convert_tip_json_file_to_csv('../yelp-data/yelp_dir/tip.json', '../yelp-data/formatted/tip.csv')
    print "Finished converting the tips json file to csv."
    print "Tips conversion took {} seconds".format((time.time() - tip_start_time))

    checkin_start_time = time.time()
    convert_checkins_json_file_to_csv('../yelp-data/yelp_dir/checkin.json', '../yelp-data/formatted/checkin.csv')
    print "Finished converting the checkin json file to csv."
    print "Checkin conversion took {} seconds".format((time.time() - checkin_start_time))

    print "Yelp data formatter process complete!"
    print "Yelp data formatter took {} seconds".format((time.time() - start_time))


if __name__ == "__main__":
    main()
