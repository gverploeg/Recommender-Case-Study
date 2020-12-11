import pandas as pd 
import numpy as np 
from surprise import Reader, Dataset
from surprise import KNNBasic, KNNWithMeans, KNNBaseline, SVD, NMF, SlopeOne, CoClustering
from surprise import SVDpp, NormalPredictor, KNNWithZScore, BaselineOnly
from surprise.model_selection import cross_validate
import logging

from baselines import GlobalMean, MeanofMeans

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a， %d %b %Y %H:%M:%S')

def get_mean_errors(cross_val_dict, rmse_key, mae_key):
    rmse = cross_val_dict[rmse_key].mean()
    mae = cross_val_dict[mae_key].mean()
    return rmse, mae

def percent_diff_errors(base_error, our_error):
    return ((base_error - our_error) / base_error) * 100

def get_SVD_model(data):
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)
    return algo

def read_item_names(filepath):
    df = pd.read_csv(filepath)
    rid_to_name = {}
    name_to_rid = {}
    for index, row in df.iterrows():
        rid_to_name[row['movieId']] = row['title']
        name_to_rid[row['title']] = row['movieId']
    return rid_to_name, name_to_rid

def show_recommendations(algo, rid_to_name, name_to_rid, movie_title):
    movie_rid = name_to_rid[movie_title]
    # logging.debug('raw_id=' + movie_rid)
    movie_inner_id = algo.trainset.to_inner_iid(movie_rid)
    # logging.debug('inner_id=' + str(movie_inner_id))
    movie_neighbors = algo.get_neighbors(movie_inner_id, 10)
    # logging.debug('neighbors_ids=' + str(movie_neighbors))
    neighbors_rids = [algo.trainset.to_raw_iid(inner_id) for inner_id in movie_neighbors]
    neighbors_movies = [rid_to_name[raw_id] for raw_id in neighbors_rids]
    print('The 10 recommendations if you like {}:'.format(movie_title))
    for movie in neighbors_movies:
        print(movie)

# class FunkSVD(SVD):
#     def __init__(self):
#         SVD.__init__(self)

#     def train_set(self, data):
#         self.trainset = data.build_full_trainset()
#         return self.trainset

#     def fit(self):
#         SVD.fit(self, self.trainset)
#         return self

if __name__ == '__main__':
    df = pd.read_csv('../data/ml-latest-small/ratings.csv').drop(columns='timestamp')
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)

    a = cross_validate(GlobalMean(), data, measures=['RMSE', 'MAE'], cv=5, verbose=False)
    global_rmse, global_mae = get_mean_errors(a, 'test_rmse', 'test_mae')

    b = cross_validate(MeanofMeans(), data, measures=['RMSE', 'MAE'], cv=5, verbose=False)
    mom_rmse, mom_mae = get_mean_errors(b, 'test_rmse', 'test_mae')

    # benchmark = []
    # for algorithm in [SVD(), SVDpp(), SlopeOne(), NMF(), NormalPredictor(), KNNBaseline(), KNNBasic(), KNNWithMeans(), KNNWithZScore(), BaselineOnly(), CoClustering()]:
    #     results = cross_validate(algorithm, data, measures=['RMSE'], cv=5, verbose=False)
        
    #     # Get results & append algorithm name
    #     tmp = pd.DataFrame.from_dict(results).mean(axis=0)
    #     tmp = tmp.append(pd.Series([str(algorithm).split(' ')[0].split('.')[-1]], index=['Algorithm']))
    #     benchmark.append(tmp)
    
    # surprise_results = pd.DataFrame(benchmark).set_index('Algorithm').sort_values(by='test_rmse')
    # global_mean_rmse = global_rmse
    # mom_mean_rmse = mom_rmse
    # surprise_results['%_Improvement_Over_GlobalMean'] = ((global_mean_rmse-surprise_results['test_rmse'])/global_mean_rmse)*100
    # surprise_results['%_Improvement_Over_MeanOfMeans'] = ((mom_mean_rmse-surprise_results['test_rmse'])/mom_mean_rmse)*100
    # surprise_results.rename(columns={'test_rmse': '5-Fold_CrossVal_RMSE', 
    #                          'fit_time': 'Fit_Time', 'test_time': 'Test_Time'}, 
    #                              inplace=True)
    # cols = ['5-Fold_CrossVal_RMSE', '%_Improvement_Over_GlobalMean', '%_Improvement_Over_MeanOfMeans',
    #             'Fit_Time', 'Test_Time']
    # surprise_results = surprise_results[cols]

    rid_to_name, name_to_rid = read_item_names('../data/ml-latest-small/movies.csv')
    algo = get_SVD_model(data)
    show_recommendations(algo, rid_to_name, name_to_rid, 'Forrest Gump (1994)')