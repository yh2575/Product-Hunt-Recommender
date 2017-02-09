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


# def recommend_result():
#
#
#
#
#     nn = model.get_similar_items(raw_data, 5)
#     nn_pd = nn.to_dataframe()
#     rec = X[X['id'].isin(nn_pd.similar)][['id', 'name', 'tagline','date', 'votes_count']]
#     rec['url']= 'https://www.producthunt.com/posts/' + rec['id'].astype('str')
#     page = rec['url'].values.tolist()
#
#     return render_template('recommend_new.html')
# @app.route('/recommend_new', methods=['POST'])
# def itemitem_recommend():
#
#
#     return render_template('recommend_new_result.html', page=page)



#
# @app.route('/recommend_new')
# def recommend2():
#     '''Home page'''
#     return render_template('recommend_new.html')

#
#
# @app.route('/recommend-vip', methods=['POST'] )
# def submission_page():
#     '''outputs the 11 most similar subreddits and color codes the text.
#        red for offensive, green for not offensive'''
#
#     product_id = filterinput(request.form['newtext'])
#
#     #load model
#     model = gl.load_model('item_content_recommender')
#     rf = gl.load_model('~/Desktop/producthunt/rf_rec')
#
#
#     #find most similar products
#     # prediction, simSubredditList = mostSimilarDoc(model,tweet,k,threshold)
#
#     nn = model.get_similar_items(raw_data, 5)
#     nn_pd = nn.to_dataframe()
#     rec = X[X['id'].isin(nn_pd.similar)][['id', 'name', 'tagline','date', 'votes_count']]
#     rec['url']= 'https://www.producthunt.com/posts/' + rec['id'].astype('str')
#     page = 'similar products are {}. <br>'.format(rec)
#
    #a list of the classes of the subreddit, hate or not hate.
    #used to tell html code what color output link should be.

    #
    #
    # return render_template('index2.html', tweet=product_id ,subreddit=page)


if __name__ == '__main__':


    # Start Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)


# if __name__ == '__main__':
#     # Register for pinging service
#     ip_address = socket.gethostbyname(socket.gethostname())
#     print "attempting to register %s:%d" % (ip_address, PORT)
#     register_for_ping(ip_address, str(PORT))
#
#     # Start Flask app
#     app.run(host='0.0.0.0', port=PORT, debug=True)

# Joanna Hou [1:58 PM]
# from flask import Flask, request, render_template
# import json
# import graphlab as gl
# import socket
# import time
# import pandas as pd
#
#
# app = Flask(__name__)
# PORT = 8080
# model = gl.load_model('item_content_recommender')
# rf = gl.load_model('~/Desktop/producthunt/rf_rec')
#
# post = pd.read_csv('~/Desktop/producthunt/subsetdata/PostsForAnalysis.txt')
# columns = post.columns
# X = post[columns]
# X = X.drop_duplicates()
#
#
# @app.route('/home')
# def index():
#     return render_template('index.html')
#
# @app.route('/submission_page')
# def submission_page():
#
#     return '''
#         The product you viewed is:
#        <form action="/recommend" method='POST' >
#            <input type="text" name="user_input" />
#            <input type="submit" />
#        </form>
#
#         Your user_id is:
#         <form action="/recommend_rf" method='POST' >
#            <input type="text" name="user_id" />
#            <input type="submit" />
#        </form>
#        '''
#

#
# @app.route('/recommend_rf', methods=['POST'])
# def rf_recommend():
#     raw_data =  [int(request.form['user_id'])]
#     rec = rf.recommend(users=raw_data, k=5)
#     nn = rec.to_dataframe()
#     nn['url']= 'https://www.producthunt.com/posts/' + nn['product_id'].astype('str')
#
#     page = 'similar products are {}. <br>'.format(nn.url)
#     return page
#
# def evaluation():
#     #topic modeling on tagline or comments
#     pass
#
# # @app.route('/about_us')
# # def about_us():
# #     return render_template('about_us.html')
#
# if __name__ == '__main__':
#
#
#    # Start Flask app
#    app.run(host='0.0.0.0', port=8080, debug=True)
#
#
# # if __name__ == '__main__':
# #     # Register for pinging service
# #     ip_address = socket.gethostbyname(socket.gethostname())
# #     print "attempting to register %s:%d" % (ip_address, PORT)
# #     register_for_ping(ip_address, str(PORT))
# #
# #     # Start Flask app
# #     app.run(host='0.0.0.0', port=PORT, debug=True)
#
