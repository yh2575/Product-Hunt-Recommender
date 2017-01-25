import requests
import sys
import json
import pandas as pd
import ijson


def get_many(link,filename,  token):

    for i in xrange(1, 82000):
        print 'post_id', i
        token['post_id'] = i
        response = requests.get(link.format(i), params=token)
        data = response.json()
        append_to_json('votes.json', data)

def append_to_json(filename, data):
    line = json.dumps(data).replace('\r', '').replace('\n', '')
    open(filename, 'a+b').write(line + '\r\n')

def open_json_file(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data

if __name__ == '__main__':
    token = {
        "access_token" : "517fa0e53de79da4180a4b27d3d4000fee4e2dea1f6fdd026b311bfafbd0e163",
        "token_type" : "bearer",
    }
    base = "https://api.producthunt.com/v1/posts/{}/votes"
    get_many(base, 'votes.json', token)

    ## need post_id
    ## need user_id

    ## scraped until 35950, need to dump repetitive rows 30000-35950