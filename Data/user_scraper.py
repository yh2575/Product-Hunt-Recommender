import requests
import sys
import json
import pandas as pd


def get_many(link,filename,  token):
  '''get user data from user_api'''
  
    for i in xrange(1,702612):
        print 'user_id', i
        token['id'] = i
        response = requests.get(link+'{}'.format(i), params=token)
        data = response.json()
        append_to_json('user.json', data)

def append_to_json(filename, data):
    line = json.dumps(data).replace('\r', '').replace('\n', '')
    open(filename, 'a+b').write(line + '\r\n')

def open_json_file(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data

if __name__ == '__main__':
    token = {ask me
    }
    base = "https://api.producthunt.com/v1/users/"
    get_many(base, 'user.json', token)
