import pandas as pd
import seaborn as sns
import json
import sys, os
import requests

def get_many(link,filename,  payload):
    '''scrap comments data for 8199 pages
       note: only max 50 comments per page'''
    for i in xrange(1033, 8200):
        offset = i
        payload['offset'] = i
        response = requests.get(link+'?page={}'.format(i), params=payload)
        if response.status_code != 200:
            print 'Got up to offest', i
            print 'Failed.', response.status_code
        else:
            print 'page_number', i
            print '---------------------------------------------'
            record_number = 0
            for item in response.json()["comments"]:
                append_to_json('commentsdata.json', item)

def append_to_json(filename, data):
    line = json.dumps(data).replace('\r', '').replace('\n', '')
    open(filename, 'a+b').write(line + '\r\n')

def open_json_file(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data

def read_s3_data(filename):
    '''
    Input: filename
    Output: local json file

    this is to download files from s3 to the local enviroment
    '''
    # local_path = '~/Desktop/producthunt/'
    access_key, secret_access_key = get_aws_access()
    conn = boto.connect_s3(access_key, secret_access_key)
    bucketname = 'producthuntdata'
    bucket = conn.get_bucket(bucketname)
    bucket_list = bucket.list()
    for l in bucket_list:
        keyString = str(l.key)
        if not os.path.exists(keyString):
            result = l.get_contents_to_filename(keyString)
    return result


def s3_upload_files(bucketname, *args):
    '''
    Input: String, List of Strings
    Output: None
    With the first string as the name of a bucket on s3, upload each individual
    file from the filepaths listed in the list of strings.
    '''

    access_key, secret_access_key = get_aws_access()
    conn = boto.connect_s3(access_key, secret_access_key)

    if conn.lookup(bucketname) is None:
        bucket = conn.create_bucket(bucketname, policy='public-read')
    else:
        bucket = conn.get_bucket(bucketname)

    for filename in args:
        key = bucket.new_key(filename)
        key.set_contents_from_filename(filename)

def get_aws_access():
    '''
    Input: None
    Output: String, String
    Read in the .json file where the aws access key and secret access key are stored.
    Output the access and secret_access_key.
    '''

    with open('awskey.json') as f:
        data = json.load(f)
        access_key = data['access-key']
        secret_access_key = data['secret-access-key']

    return access_key, secret_access_key

def convert_to_dataframe(df):
    ''' the json file downloaded from S3 needs further parsing and processing
        before tunrning into a dataframe'''
    with open(df, 'rb') as f:
        data = f.readlines()
    # remove the trailing "\n" from each line
        data = map(lambda x: x.rstrip(), data)
    data_json_str = "[" + ','.join(data) + "]"
    data_df = pd.read_json(data_json_str)
    return data_df

if __name__ == '__main__':
    # filepath = 'https://s3.amazonaws.com/producthuntdata/comments.json'
    link = 'https://api.producthunt.com/v1/comments'
    token = {
    "access_token" : "517fa0e53de79da4180a4b27d3d4000fee4e2dea1f6fdd026b311bfafbd0e163",
    "token_type" : "bearer"}
    #scrap comments from API
    filename = 'commentsdata.json'
    get_many(link,filename,token)
    #upload comments to S3
    filepath1 = 'commentsdata.json'
    s3_upload_files(bucketname, filepath1)

    #download data from s3
    # f = read_s3_data(filename)

    #convert data to pd format
    # df = convert_to_dataframe('comments.json')
