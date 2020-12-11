# import logging

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a， %d %b %Y %H:%M:%S')
# import os
# import io
# from surprise import KNNWithMeans
# from surprise import Dataset


# # Training recommendation model steps: 1
# def getSimModle():
#     # Default loading of movielens dataset
#     data = Dataset.load_builtin('ml-100k')
#     trainset = data.build_full_trainset()
#     #Using pearson_baseline method to calculate similarity False calculates similarity between movies based on item
#     # sim_options = {'name': 'pearson_baseline', 'user_based': False}
#     ##Using KNNBaseline algorithm
#     algo = KNNWithMeans()
#     #Training model
#     algo.fit(trainset)
#     return algo


# # Getting id to name mapping steps: 2
# def read_item_names():
#     """
#     //Get the mapping of movie name to movie id and movie id to movie name
#     """
#     file_name = (os.path.expanduser('~') +
#                  '/.surprise_data/ml-100k/ml-100k/u.item')
#     rid_to_name = {}
#     name_to_rid = {}
#     with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
#         for line in f:
#             line = line.split('|')
#             rid_to_name[line[0]] = line[1]
#             name_to_rid[line[1]] = line[0]
#     return rid_to_name, name_to_rid


# # Recommendation steps for related movies based on the previous training model:3
# def showSimilarMovies(algo, rid_to_name, name_to_rid):
#     # Get raw_id of the movie Toy Story (1995)
#     toy_story_raw_id = name_to_rid['Toy Story (1995)']
#     logging.debug('raw_id=' + toy_story_raw_id)
#     #Converting raw_id of a movie to the internal ID of the model
#     toy_story_inner_id = algo.trainset.to_inner_iid(toy_story_raw_id)
#     logging.debug('inner_id=' + str(toy_story_inner_id))
#     #Get Recommended Movies from Model Here are 10
#     toy_story_neighbors = algo.get_neighbors(toy_story_inner_id, 10)
#     logging.debug('neighbors_ids=' + str(toy_story_neighbors))
#     #The internal id of the model is converted to the actual movie id
#     neighbors_raw_ids = [algo.trainset.to_raw_iid(inner_id) for inner_id in toy_story_neighbors]
#     #Get a movie id list or a movie recommendation list
#     neighbors_movies = [rid_to_name[raw_id] for raw_id in neighbors_raw_ids]
#     print('The 10 nearest neighbors of Toy Story are:')
#     for movie in neighbors_movies:
#         print(movie)


# if __name__ == '__main__':
#     # Get the mapping of id to name
#     rid_to_name, name_to_rid = read_item_names()

#     # Training Recommendation Model
#     algo = getSimModle()

#     ##Display related movies
#     showSimilarMovies(algo, rid_to_name, name_to_rid)

# from surprise import KNNWithMeans
# from surprise import Dataset
# from surprise.model_selection.validation import cross_validate

# data = Dataset.load_builtin('ml-100k')
# trainset = data.build_full_trainset()
# algo = KNNWithMeans()
# algo.fit(trainset)
# cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

import pandas as pd 
import numpy as np 
from surprise import Reader, Dataset
from surprise import KNNBasic, KNNWithMeans, KNNBaseline, SVD, NMF, SlopeOne, CoClustering
from surprise.model_selection import cross_validate

from baselines import GlobalMean, MeanofMeans

def get_mean_errors(cross_val_dict, rmse_key, mae_key):
    rmse = cross_val_dict[rmse_key].mean()
    mae = cross_val_dict[mae_key].mean()
    return rmse, mae

def percent_diff_errors(base_error, our_error):
    return ((base_error - our_error) / base_error) * 100


if __name__ == '__main__':
    df = pd.read_csv('../data/ml-latest-small/ratings.csv').drop(columns='timestamp')
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)
    
    # # print("\nGlobal Mean...")
    # a = cross_validate(GlobalMean(), data, measures=['RMSE', 'MAE'], cv=5)
    # global_rmse, global_mae = get_mean_errors(a, 'test_rmse', 'test_mae')
    # # print('Mean RMSE: {}'.format(get_mean_error(a, 'test_rmse')))
    # # print('Mean MAE: {}'.format(get_mean_error(a, 'test_mae')))

    # # print("\nMeanOfMeans...")
    b = cross_validate(MeanofMeans(), data, measures=['RMSE', 'MAE'], cv=5)
    mom_rmse, mom_mae = get_mean_errors(b, 'test_rmse', 'test_mae')
    # print('Mean RMSE: {}'.format(get_mean_error(b, 'test_rmse')))
    # print('Mean MAE: {}'.format(get_mean_error(b, 'test_mae')))

    c = cross_validate(KNNBasic(), data, measures=['RMSE', 'MAE'], cv=5)
    knn_rmse, knn_mae = get_mean_errors(c, 'test_rmse', 'test_mae')

    # print("\nKNNWithMeans...")
    d = cross_validate(KNNWithMeans(), data, measures=['RMSE', 'MAE'], cv=5)
    knnmean_rmse, knnmean_mae = get_mean_errors(d, 'test_rmse', 'test_mae')
    # print('Mean RMSE: {}'.format(get_mean_error(c, 'test_rmse')))
    # print('Mean MAE: {}'.format(get_mean_error(c, 'test_mae')))

    e = cross_validate(KNNBaseline(), data, measures=['RMSE', 'MAE'], cv=5)
    knnbase_rmse, knnbase_mae = get_mean_errors(e, 'test_rmse', 'test_mae')

    f = cross_validate(SVD(), data, measures=['RMSE', 'MAE'], cv=5)
    svd_rmse, svd_mae = get_mean_errors(f, 'test_rmse', 'test_mae')

    g = cross_validate(SlopeOne(), data, measures=['RMSE', 'MAE'], cv=5)
    slope_rmse, slope_mae = get_mean_errors(g, 'test_rmse', 'test_mae')

    h = cross_validate(CoClustering(), data, measures=['RMSE', 'MAE'], cv=5)
    cluster_rmse, cluster_mae = get_mean_errors(h, 'test_rmse', 'test_mae')

    print('\nPercent Changes:')
    # print('GolbalMean vs MeanOfMeans RMSE: {}'.format(percent_diff_errors(global_rmse, mom_rmse)))
    # print('GlobalMean vs MeanofMeans MAE: {}'.format(percent_diff_errors(global_mae, mom_mae)))
    print('\n')
    print('KNNBasic vs MeanOfMeans RMSE: {}'.format(percent_diff_errors(mom_rmse, knn_rmse)))
    print('KNNBasic vs MeanOfMeans MAE: {}'.format(percent_diff_errors(mom_mae, knn_mae)))
    print('\n')
    print('KNNWithMeans vs MeanOfMeans RMSE: {}'.format(percent_diff_errors(mom_rmse, knnmean_rmse)))
    print('KNNWithMeans vs MeanOfMeans MAE: {}'.format(percent_diff_errors(mom_mae, knnmean_mae)))
    print('\n')
    print('KNNBaseline vs MeanOfMeans RMSE: {}'.format(percent_diff_errors(mom_rmse, knnbase_rmse)))
    print('KNNBaseline vs MeanOfMeans MAE: {}'.format(percent_diff_errors(mom_mae, knnbase_mae)))
    print('\n')
    print('FunkSVD vs MeanOfMeans RMSE: {}'.format(percent_diff_errors(mom_rmse, svd_rmse)))
    print('FunkSVD vs MeanOfMeans MAE: {}'.format(percent_diff_errors(mom_mae, svd_mae)))
    # print('\n')
    # print('SlopeOne vs MeanOfMeans RMSE: {}'.format(percent_diff_errors(mom_rmse, slope_rmse)))
    # print('SlopeOne vs MeanOfMeans MAE: {}'.format(percent_diff_errors(mom_mae, slope_mae)))
    # print('\n')
    # print('CoClustering vs MeanOfMeans RMSE: {}'.format(percent_diff_errors(mom_rmse, cluster_rmse)))
    # print('CoClustering vs MeanOfMeans MAE: {}'.format(percent_diff_errors(mom_mae, cluster_mae)))
 