import io
import json
import os


def convert_business_json_file_to_csv(old_file_path, new_file_path):
    write_dir = os.path.dirname(new_file_path)
    if not os.path.isdir(write_dir):
        os.mkdir(write_dir)
    with io.open(new_file_path, 'w', encoding='utf-8') as new_f:
        new_f.write(u'biz_id,name,neighborhood,address,city,state,postal_code,latitude,longitude,' \
                    u'stars,is_open,monday_hours,tuesday_hours,wednesday_hours,thursday_hours,friday_hours,' \
                    u'saturday_hours,sunday_hours\n')
        with open(old_file_path, 'r') as old_f:
            for line in old_f:
                biz_json = json.loads(line)
                biz_cvs = u'{biz_id},{name},{neighborhood},{address},{city},{state},' \
                          u'{postal_code},{latitude},{longitude},{stars},{is_open},{monday_hours},' \
                          u'{tuesday_hours},{wednesday_hours},{thursday_hours},{friday_hours},{saturday_hours},' \
                          u'{sunday_hours}\n'.format(biz_id=biz_json['business_id'].replace(',', ' '),
                                                     name=biz_json['name'].replace(',', ' '),
                                                     neighborhood=biz_json['neighborhood'].replace(',', ' '),
                                                     address=biz_json['address'].replace(',', ' '),
                                                     city=biz_json['city'].replace(',', ' '),
                                                     state=biz_json['state'].replace(',', ' '),
                                                     postal_code=biz_json['postal_code'].replace(',', ' '),
                                                     latitude=biz_json['latitude'],
                                                     longitude=biz_json['longitude'],
                                                     stars=biz_json['stars'],
                                                     is_open=biz_json['is_open'],
                                                     monday_hours=biz_json['hours'].get('Monday', ''),
                                                     tuesday_hours=biz_json['hours'].get('Tuesday', ''),
                                                     wednesday_hours=biz_json['hours'].get('Wednesday', ''),
                                                     thursday_hours=biz_json['hours'].get('Thursday', ''),
                                                     friday_hours=biz_json['hours'].get('Friday', ''),
                                                     saturday_hours=biz_json['hours'].get('Saturday', ''),
                                                     sunday_hours=biz_json['hours'].get('Sunday', ''))
                new_f.write(biz_cvs)


def main():
    print "starting main process"
    convert_business_json_file_to_csv('yelp-data/yelp_dir/business.json', 'yelp-data/formatted/business.csv')
    print "\n finished the process"


if __name__ == "__main__":
    main()
