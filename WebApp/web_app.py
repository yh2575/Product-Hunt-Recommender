from flask import Flask, request, render_template,redirect

import json
import graphlab as gl
import socket
import time
import pandas as pd


app = Flask(__name__)

PORT = 8080


post = pd.read_csv('~/Desktop/producthunt/subsetdata/PostsForAnalysis.txt')
columns = post.columns
X = post[columns]
X = X.drop_duplicates()

model = gl.load_model('item_content_recommender')
rf = gl.load_model('~/Desktop/producthunt/rf_rec')



# home page
@app.route('/')
def welcome():
    '''Home page'''
    return render_template('home.html')



@app.route('/recommend_new')
def recommend_new():


    # raw_data = [int(request.form['user_input'])]
    # raw_data = [2345]

    return render_template('recommend_new.html')

@app.route('/recommend', methods=['POST'])
def recommend():

    raw_data = [int(request.form['user_input'])]
    nn = model.get_similar_items(raw_data, 5)
    nn_pd = nn.to_dataframe()
    rec = X[X['id'].isin(nn_pd.similar)][['id', 'name', 'tagline','date', 'votes_count']]
    rec['url']= 'https://www.producthunt.com/posts/' + rec['id'].astype('str')

    page = rec['url'].values.tolist()
    product_name = rec['name'].values.tolist()

    return render_template('recommend_result.html', id=raw_data, result=page, name=product_name)



if __name__ == '__main__':


    # Start Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)


