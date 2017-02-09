import numpy as np
import graphlab as gl
import pandas as pd
import matplotlib.pyplot as plt
from itemitem_rec import data_load, data_process


def train_test_split(df):
    t, test = gl.recommender.util.random_split_by_user(df, 'user_id', 'product_id')
    train, val = gl.recommender.util.random_split_by_user(t, 'user_id', 'product_id')
    return train, val, test

def rf_model(train, val):
    X = data_load()
    X_new, X_scaler = data_process(X)

    columns = X_new.columns

    X_new['product_id']=X_new['id']
    X_new.pop('id')
    train1 = train.to_dataframe()
    all_product_train= pd.merge(train1, X_new, how='left', on='product_id')


    model = gl.ranking_factorization_recommender.create(train1,
        item_id = 'product_id',target='votes',solver='ials', item_data=all_product_train)
    model = gl.ranking_factorization_recommender.create(train,
       item_id = 'product_id',target='votes',solver='ials', num_factors=100, regularization=0.0001)

    rec = model.recommend(items=[7063]) #eg

    model.evaluate(val)
    view = model.views.overview(observation_data=train, validation_set=val)
    view.show()
    return model,rec


    model.evaluate(val)
    # view = model.views.overview(observation_data=train, validation_set=val)
    # view.show()
    rec = model.recommend(items=[7063])
    model.save('rf_rec')

def params_search(train, val):
    X = data_load()
    X_new, X_scaler = data_process()

    columns = X_new.columns
    rating = pd.read_csv('data_40.csv')
    X_new['product_id']=X_new['id']
    X_new.pop('id')

    all_product= pd.merge(rating, X_new, how='left', on='product_id')
    train, val, test = train_test_split(all_product)

    params = dict([('target', 'votes'),
                   ('num_factors', [8, 16, 32, 64]),
                   ('regularization', [1e-09, 1e-06]),
                   ('max_iterations', [15, 25, 50]),
                   ('user_id', 'user_id'),
                   ('item_id', 'product_id') ])
    job = gl.grid_search.create((train, val),
                                gl.ranking_factorization_recommender.create,
                                params)




if __name__ == "__main__":
    df = gl.SFrame.read_csv('data_user30.csv')
    train, val, test = train_test_split(df)
    rec1 = rf_model(train, val)
    # rec2 = item_item_recommender(train, val)


