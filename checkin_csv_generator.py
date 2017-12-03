import json
import io
import os


def convert_checkins_json_file_to_csv(json_file_path, csv_file_path):
    """
    Writes the checkin.json file into a csv
    :param json_file_path: (str) path to the checkin.json file
    :param csv_file_path: (str) path to the new csv file
    :return:
    """
    write_dir = os.path.dirname(csv_file_path)
    if not os.path.isdir(write_dir):
        os.mkdir(write_dir)
    with io.open(csv_file_path, 'w', encoding='utf-8') as new_f:
        new_f.write(u'biz_id,mon_morning,mon_afternoon,mon_evening,mon_late,'
                    u'tue_morning,tue_afternoon,tue_evening,tue_late,'
                    u'wed_morning,wed_afternoon,wed_evening,wed_late,'
                    u'thu_morning,thu_afternoon,thu_evening,thu_late,'
                    u'fri_morning,fri_afternoon,fri_evening,fri_late,'
                    u'sat_morning,sat_afternoon,sat_evening,sat_late,'
                    u'sun_morning,sun_afternoon,sun_evening,sun_late\n')
        with open(json_file_path, 'r') as old_f:
            for line in old_f:

                checkin_json = json.loads(line)
                biz_id = checkin_json['business_id']
                times = checkin_json.get('time', {})

                days_dict = {}
                hours_dict = {
                    'late': (0, 6),
                    'morning': (6, 12),
                    'afternoon': (12, 18),
                    'evening': (18, 24)
                }

                for day, hours in times.iteritems():
                    for hour, count in hours.iteritems():
                        hour_val = int(hour.split(':')[0])
                        if hours_dict['late'][0] <= hour_val < hours_dict['late'][1]:
                            days_dict[day + '_late'] = str(count + int(days_dict.get(day + '_late', '0')))
                        elif hours_dict['morning'][0] <= hour_val < hours_dict['morning'][1]:
                            days_dict[day + '_morning'] = str(count + int(days_dict.get(day + '_morning', '0')))
                        elif hours_dict['afternoon'][0] <= hour_val < hours_dict['afternoon'][1]:
                            days_dict[day + '_afternoon'] = str(count + int(days_dict.get(day + '_afternoon', '0')))
                        elif hours_dict['evening'][0] <= hour_val <= hours_dict['evening'][1]:
                            days_dict[day + '_evening'] = str(count + int(days_dict.get(day + '_evening', '0')))
                        else:
                            print "Didn't find any counts for {}, {}, {}".format(biz_id, day, hour)
                checkin_csv = u'{biz_id},{mon_early},{mon_afternoon},{mon_evening},{mon_late},' \
                              u'{tue_early},{tue_afternoon},{tue_evening},{tue_late},' \
                              u'{wed_early},{wed_afternoon},{wed_evening},{wed_late},' \
                              u'{thu_early},{thu_afternoon},{thu_evening},{thu_late},' \
                              u'{fri_early},{fri_afternoon},{fri_evening},{fri_late},' \
                              u'{sat_early},{sat_afternoon},{sat_evening},{sat_late},' \
                              u'{sun_early},{sun_afternoon},{sun_evening},{sun_late}\n'.format(
                    biz_id=biz_id,
                    mon_early=days_dict.get('Monday_morning', '0'),
                    mon_afternoon=days_dict.get('Monday_afternoon', '0'),
                    mon_evening=days_dict.get('Monday_evening', '0'),
                    mon_late=days_dict.get('Monday_late', '0'),

                    tue_early=days_dict.get('Tuesday_morning', '0'),
                    tue_afternoon=days_dict.get('Tuesday_afternoon', '0'),
                    tue_evening=days_dict.get('Tuesday_evening', '0'),
                    tue_late=days_dict.get('Tuesday_late', '0'),

                    wed_early=days_dict.get('Wednesday_morning', '0'),
                    wed_afternoon=days_dict.get('Wednesday_afternoon', '0'),
                    wed_evening=days_dict.get('Wednesday_evening', '0'),
                    wed_late=days_dict.get('Wednesday_late', '0'),

                    thu_early=days_dict.get('Thursday_morning', '0'),
                    thu_afternoon=days_dict.get('Thursday_afternoon', '0'),
                    thu_evening=days_dict.get('Thursday_evening', '0'),
                    thu_late=days_dict.get('Thursday_late', '0'),

                    fri_early=days_dict.get('Friday_morning', '0'),
                    fri_afternoon=days_dict.get('Friday_afternoon', '0'),
                    fri_evening=days_dict.get('Friday_evening', '0'),
                    fri_late=days_dict.get('Friday_late', '0'),

                    sat_early=days_dict.get('Saturday_morning', '0'),
                    sat_afternoon=days_dict.get('Saturday_afternoon', '0'),
                    sat_evening=days_dict.get('Saturday_evening', '0'),
                    sat_late=days_dict.get('Saturday_late', '0'),

                    sun_early=days_dict.get('Sunday_morning', '0'),
                    sun_afternoon=days_dict.get('Sunday_afternoon', '0'),
                    sun_evening=days_dict.get('Sunday_evening', '0'),
                    sun_late=days_dict.get('Sunday_late', '0')
                )

                new_f.write(checkin_csv)
