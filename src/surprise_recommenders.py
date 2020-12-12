import pandas as pd 
import numpy as np 
from collections import defaultdict
from surprise import Reader, Dataset
from surprise import KNNBasic, KNNWithMeans, KNNBaseline, SVD, NMF, SlopeOne, CoClustering
from surprise import SVDpp, NormalPredictor, KNNWithZScore, BaselineOnly
from surprise.model_selection import cross_validate

#import the original models for the company so we can use in if name main block
from baselines import GlobalMean, MeanofMeans

#get the mean rmse and mae from the Surprise cross-val function, the dictionary only gives back the 5 folds as an array so have to take
#the mean of the array
def get_mean_errors(cross_val_dict, rmse_key, mae_key):
    rmse = cross_val_dict[rmse_key].mean()
    mae = cross_val_dict[mae_key].mean()
    return rmse, mae

#calculate the percent increase/difference between the rmse or mae (whichever error you choose) from the old model and our model
def percent_diff_errors(base_error, our_error):
    return ((base_error - our_error) / base_error) * 100

#create our KNNBaseline model since that is the one we chose
def get_KNN_model(data):
    trainset = data.build_full_trainset() #build_full_trainset is built-in to Surprise and creates a training set from data
    algo = KNNBaseline() #set the model algorithm
    algo.fit(trainset) #fit on training set
    return algo #return the fit model

#use the movies.csv file to get movie title names from unique numeric MovieID
#create two different dictionaries depending on if we need to translate title to ID and vice versa
def read_item_names(filepath):
    df = pd.read_csv(filepath)
    rid_to_name = {}
    name_to_rid = {}
    for idx, row in df.iterrows():
        rid_to_name[row['movieId']] = row['title']
        name_to_rid[row['title']] = row['movieId']
    return rid_to_name, name_to_rid

#get top movie recommendations based on a specific movie title
def show_recommendations(algo, rid_to_name, name_to_rid, movie_title, n_recs=10):
    movie_rid = name_to_rid[movie_title] #translate movie title into numeric movie ID
    movie_inner_id = algo.trainset.to_inner_iid(movie_rid) #to get the KNN you have to get this inner ID (only know from documentation)
    movie_neighbors = algo.get_neighbors(movie_inner_id, n_recs) #.get_neighbors is an attribute you can call on your model in Surprise for KNN Algos
    neighbors_rids = [algo.trainset.to_raw_iid(inner_id) for inner_id in movie_neighbors] #get the movieID for the neighbors
    neighbors_movies = [rid_to_name[raw_id] for raw_id in neighbors_rids] #translate neighbor IDs to titles
    print('The {} recommendations if you like {}:'.format(n_recs, movie_title))
    for movie in neighbors_movies: #print list of titles
        print(movie)

'''Sam's attempt at making our model as a class, didn't test'''
# class KNN(KNNBaseline):
#     def __init__(self):
#         KNNBaseline.__init__(self)

#     def train_set(self, data):
#         self.trainset = data.build_full_trainset()
#         return self.trainset

#     def fit(self):
#         KNNBaseline.fit(self, self.trainset)
#         return self

if __name__ == '__main__':
    #pandas dataframe of the ratings csv
    df = pd.read_csv('../data/ml-latest-small/ratings.csv').drop(columns='timestamp')
    #Reader class from Surprise, you have to tell it the scale that will be in the rating column
    reader = Reader(rating_scale=(0.5, 5))
    #use the reader object we made above in loading the dataframe into a data for use; Dataset is a class in surprise so that is how
    #load your own dataframe in
    data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)

    #use Surprise cross_validate with 5 folds to get back the rmse and mae measures. Verbose=False means you don't see giant printout
    #do this for the global and meanofmeans old models so we have them to compare
    a = cross_validate(GlobalMean(), data, measures=['RMSE', 'MAE'], cv=5, verbose=False)
    global_rmse, global_mae = get_mean_errors(a, 'test_rmse', 'test_mae')

    b = cross_validate(MeanofMeans(), data, measures=['RMSE', 'MAE'], cv=5, verbose=False)
    mom_rmse, mom_mae = get_mean_errors(b, 'test_rmse', 'test_mae')

    '''this section is commented out as it takes a while to run but creates the dataframe we used for our table of models'''
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
        #this calculates the %improvement, i didn't do the function just wrote it in here
    # surprise_results['%_Improvement_Over_MeanOfMeans'] = ((mom_mean_rmse-surprise_results['test_rmse'])/mom_mean_rmse)*100
    # surprise_results.rename(columns={'test_rmse': '5-Fold_CrossVal_RMSE', 
    #                          'fit_time': 'Fit_Time', 'test_time': 'Test_Time'}, 
    #                              inplace=True)
    # cols = ['5-Fold_CrossVal_RMSE', '%_Improvement_Over_GlobalMean', '%_Improvement_Over_MeanOfMeans',
    #             'Fit_Time', 'Test_Time'] #reorders the columns
    # surprise_results = surprise_results[cols]

    #get dictionary of movie titles and IDs to map with
    rid_to_name, name_to_rid = read_item_names('../data/ml-latest-small/movies.csv')
    #create our model as KNNBaseline on the imported data
    algo = get_KNN_model(data)
    #print out the 10 recommendations for this top movies
    print('\n')
    show_recommendations(algo, rid_to_name, name_to_rid, 'Forrest Gump (1994)', 10)
    print('\n')
    show_recommendations(algo, rid_to_name, name_to_rid, 'Shawshank Redemption, The (1994)', 10)
    print('\n')
    show_recommendations(algo, rid_to_name, name_to_rid, 'Pulp Fiction (1994)', 10)
    print('\n')
    show_recommendations(algo, rid_to_name, name_to_rid, 'Silence of the Lambs, The (1991)', 10)
    print('\n')
    show_recommendations(algo, rid_to_name, name_to_rid, 'Matrix, The (1999)', 10)
    print('\n')
    show_recommendations(algo, rid_to_name, name_to_rid, 'Star Wars: Episode IV - A New Hope (1977)', 10)
    print('\n')
    show_recommendations(algo, rid_to_name, name_to_rid, 'Jurassic Park (1993)', 10)
    print('\n')
    show_recommendations(algo, rid_to_name, name_to_rid, 'Braveheart (1995)', 10)
