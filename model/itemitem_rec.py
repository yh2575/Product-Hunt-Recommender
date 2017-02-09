import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import NMF
# from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
# from sklearn.decomposition import NMF
from sklearn import preprocessing
from sklearn.metrics.pairwise import cosine_similarity
import graphlab as gl
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.cross_validation import train_test_split

#this is a recommender from cosine similarity
def data_load():
    post = pd.read_csv('subsetdata/PostsForAnalysis.txt')
    columns = post.columns
    X = post[columns]
    X = X.drop_duplicates()
    return X

def norm(df, col):
    df[col] = (df[col] - df[col].mean())/(df[col].max() - df[col].min())
    return df


def data_process(X):
    #dummify columns
    for elem in X['time_of_day'].unique():
        X[str(elem)] = X['time_of_day'] == elem
    for elem in X['day'].unique():
        X[str(elem)] = X['day'] == elem
    for elem in X['thumbnail_type'].unique():
        X[str(elem)] = X['thumbnail_type'] == elem
    #drop columns are not float/int/bool
    X_new = X.drop(['date', 'day', 'created_at', 'time_of_day', 'name', 'tagline', 'thumbnail_type', 'product_state'], axis=1)
    #replace nan by False
    X_new = X_new.fillna(False)
    columns1 = X_new.columns
    #binarize all bool values
    X_new = X_new[columns1].astype(int)
    cols_norm = ['comments_count', 'num_makers', 'num_topics'] #columns need to be normalized
    X_scaler = norm(X_new, cols_norm)
    return X_new, X_scaler

#dimention reduction?

def item_content_recommender(X_scaler, X_new, X):
    # supress votes
    columns1 = X_new.columns
    sc = pd.DataFrame(X_scaler, columns=columns1)
    sc['id']=X_new['id']
    sf = gl.SFrame(sc)
    model = gl.recommender.item_content_recommender.create(sf, item_id='id')
    raw_data = [42943]
    nn = model.get_similar_items(raw_data, 5)
    nn_pd = nn.to_dataframe()
    rec = X[X['id'].isin(nn_pd.similar)]
    model.save('item_content_recommender')

    return model, rec
#can we use GB to get feature importance first? mixing models?
def item_item_recommender(X_scaler, X_new, X):
    columns1 = X_new.columns
    rating = pd.read_csv('data_40.csv')
    # rp = rating.product_id
    # X_item = X_new.loc[X_new['id'].isin(rp)][columns1]
    # rating_matrix = rating.pivot(index='user_id', columns='product_id', values='votes' )
    X_new['product_id']=X_new['id']
    X_new.pop('id')
    all_product= pd.merge(rating, X_new, how='left', on='product_id')
    y = all_product['votes']
    x = all_product.drop('votes', axis=1)
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)
    gb = GradientBoostingRegressor(min_samples_leaf=3, random_state=0).fit(X_train, y_train)
    print 'RMSE: ', np.sqrt(mean_squared_error(y_test, gb.predict(X_test)))
    feat_imp = gb.feature_importances_
    feat_scores = pd.DataFrame({'Fraction of Samples Affected' : gb.feature_importances_},
                           index=x.columns)
    feat_scores = feat_scores.sort_values(by='Fraction of Samples Affected')
    feat_scores.plot(kind='barh', color='green')
    weights = dict(zip(X.columns, gb.feature_importances_))

    all_product.corr()
    sf = gl.SFrame(all_product)
    model = gl.recommender.item_content_recommender.create(sf, item_id='product_id', weights=weights)
    recs = model.recommend_from_interactions([int(raw_input('please input an item id: '))], 5, diversity=2)
    model.save('item_item_recommender')
    return model, recs


# def recommend(X, y, n=5):
#     # Calculate similarity to all of the hikes
#     # average similarities
#     # return top 5
#     indx_id = X['id']
#     X = X.drop('id', axis=1)
#     y = raw_input('please input a product id: ')
#     y = y.drop('id', axis=1)
#     cs = cosine_similarity(X, y).mean(axis=1)
#     rec_index= np.argsort(cs)[-n:][::-1]
#     recommendations = indx_id.ix[rec_index]
#     return recommendations

def plotting(X_new):
    kmeans = KMeans(n_clusters=5).fit(X_new)
    X_new['kmeans_label'] = kmeans.labels_
    color_map = {0: 'green', 1: 'red', 2: 'yellow', 3: 'blue', 4: 'purple'}
    plt.figure(figsize=(8,6))
    plt.scatter(X_new['votes_count'],X_new['num_topics'], c=X_new['kmeans_label'].map(color_map))
    plt.xlabel('votes_count')
    plt.ylabel('num_topics')
    plt.title('votes_count vs num_topics')
    plt.show()
    plt.savefig('votes_count vs num_topics')

    plt.figure(figsize=(8,6))
    plt.scatter(X_new['votes_count'],X_new['comments_count'], c=X_new['kmeans_label'].map(color_map))
    plt.xlabel('votes_count')
    plt.ylabel('comments_count')
    plt.title('votes_count vs comments_count')
    plt.show()
    plt.savefig('votes_count vs comments_count')
    # user_id small tend to vote more
    plt.figure(figsize=(8,6))
    plt.scatter(X_new['votes_count'],X_new['user_id'], c=X_new['kmeans_label'].map(color_map))
    plt.xlabel('votes_count')
    plt.ylabel('user_id')
    plt.title('votes_count vs user_id')
    plt.show()
    plt.savefig('votes_count vs user_id')

    # user_id small tend to vote more

# def train_test_split(df):
#     t, test = gl.recommender.util.random_split_by_user(df, 'user_id', 'product_id')
#     train, val = gl.recommender.util.random_split_by_user(t, 'user_id', 'product_id')
#     return train, val, test



if __name__ =="__main__":
    X = data_load()
    X_new, X_scaler = data_process(X)
    model =  item_content_recommender(X_scaler, X_new, X)
    raw_data = [82460]
    model.recommend(raw_data)
    nn = model.get_similar_items(raw_data)
    rec = X[X['id'].isin(nn.similar)]
    # item_item_recommender(X_scaler, X_new, X)





























def item_content_recommender(train, val):
    pass

def user_user_recommender(train, val):
    pass
    ''' user comments'''

def weighted_recommender(train, val):
    pass

def test_recommender(all, test):
    pass

def recommend(trial):
    '''should give a list of products with names, tagline, url, votes'''

    pass


def vectorize(self):
    '''
    INPUT: list of cleaned, lemmatized and filtered text
    OUTPUT: cleaned up string ready to be fed into a vectorizer

    Vectorizes documents in the corpus (resources from PG, Coursera, etc.) and computes cosine similarity
    with a user's Quora profile information or Question Page
    '''

    vec = TfidfVectorizer(ngram_range = (1,5), max_features = 5000)
    #vec = TfidfVectorizer(ngram_range = (2,3), max_features=5000)
    doc_vecs_sparse = vec.fit_transform(self.df.desc.values)
    quora_vec = vec.transform(self.quora.values)
    self.distances = cosine_similarity(quora_vec, doc_vecs_sparse)[0]


def recommend(self):
    '''
    INPUT: np array of distances
    OUTPUT: names and types of recommendations
    '''

    top_ten = np.argsort(self.distances)[::-1]
    return top_ten[:20]
