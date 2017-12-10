import json
import requests
from itertools import chain, islice
import os
import glob
from Queue import Queue
from threading import Thread

config = {}
with open('../config.json', 'r') as f:
    config = json.load(f)

auth_url = 'https://api.yelp.com/oauth2/token'

resp = requests.post(auth_url, data={'client_id': config['client_id'],
                                     'client_secret': config['client_secret']})

token = resp.json()['access_token']


def chunks(iterable, n):
    "chunks(ABCDE,2) => AB CD E"
    iterable = iter(iterable)
    while True:
        # store one line in memory,
        # chain it to an iterator on the rest of the chunk
        yield chain([next(iterable)], islice(iterable, n - 1))


data_dir = '../yelp-data/yelp_dir/'
out_dir = '../yelp-data/formatted/'

files_splits = []
chunk_size = 25000
new_file_path = out_dir + '/updated_businesses.csv'

with open(out_dir + 'business.csv') as bigfile:
    for i, lines in enumerate(chunks(bigfile, chunk_size)):
        file_split = '{}.{}'.format(new_file_path, i)
        files_splits.append(file_split)
        with open(file_split, 'w') as f:
            f.writelines(lines)

index = 0
biz_ids = []
for f_name in files_splits:
    with open(f_name, 'r') as f_part:
        for line in f_part:
            index += 1
            if index > 1:
                current_count = 0
                fields = line.split(',')
                biz_id = fields[0]
                is_open = int(fields[10])
                if is_open == 1:
                    biz_ids.append(biz_id)

search_url = 'https://api.yelp.com/v3/graphql'

data = """
{
    b1: business(id: "mLwM-h2YhXl2NCgdS84_Bw") {
        name
        is_closed
    }
    b2: business(id: "gOeU8MmVBzmaOWA191hLpg") {
        name
        is_closed
    }
}
"""


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in xrange(0, len(l), n))


biz_chunks = chunks(biz_ids, 75)

call_queue = Queue(maxsize=0)
request_to_biz_id_map = {}
index = 0
for biz_id_group in biz_chunks:
    data_str = """{"""
    for biz_id in biz_id_group:
        index += 1
        request_id = "b" + str(index)
        request_to_biz_id_map[request_id] = biz_id
        data_str += """
        """ + str(request_id) + """: business(id: \"""" + biz_id + """\") {
            id
            name
            is_closed
        }
        """
    data_str += """}"""
    call_queue.put(data_str)



def consume_api(call_q, f_name):
    while not call_q.empty():
        with open(f_name, 'a') as new_f:
            new_f.write("biz_id,is_closed\n")
            post = call_q.get()
            print "starting call for " + f_name
            search_url = 'https://api.yelp.com/v3/graphql'
            resp = requests.post(search_url, headers={'Authorization': 'bearer %s' % token,
                                                      'Content-Type': 'application/graphql'},
                                 data=post)
            resp_json = resp.json()
            if 'data' in resp_json:
                data_resp = resp_json[u'data']
                if data_resp:
                    for run_id, details in data_resp.iteritems():
                        if details:
                            biz_id = request_to_biz_id_map[run_id]
                            is_closed = details['is_closed']
                            new_f.write("{biz_id},{is_closed}\n".format(biz_id=biz_id, is_closed=is_closed))
            call_q.task_done()


num_threads = 15
fnames_part = []
workers = []

print "starting api calls"
for i in range(num_threads):
    worker_f = out_dir + 'updated_closures.csv' + str(i)
    worker = Thread(target=consume_api, args=(call_queue, worker_f,))
    workers.append(worker)
    worker.setDaemon(True)
    worker.start()
    fnames_part.append(worker_f)

[x.join() for x in workers]


def combine_ratings_files(files):
    combined = []
    for f_name in files:
        with open(f_name, 'r') as reader_f:
            index = 0
            for red_line in reader_f:
                index += 1
                if index > 1:
                    fields = red_line.split(',')
                    biz_id = fields[0]
                    is_open = fields[1].replace('\n', '')
                    combined.append((biz_id, is_open))
    return combined

all_statuses = combine_ratings_files(fnames_part)

with open(out_dir + 'updated_closures.csv', 'w') as new_f:
    new_f.write("biz_id,is_closed\n")
    for status in all_statuses:
        new_f.write("{biz_id},{is_closed}\n".format(biz_id=status[0], is_closed=status[1]))

for thread_file in fnames_part:
    os.remove(thread_file)
