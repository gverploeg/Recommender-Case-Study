#!/usr/bin/env python

"""
http://surprise.readthedocs.io/en/stable/building_custom_algo.html
"""

import sys
import numpy as np
import pandas as pd 
from surprise import AlgoBase, Dataset, Reader
from surprise.model_selection.validation import cross_validate

class GlobalMean(AlgoBase):
    def __init__(self):

        # Always call base method before doing anything.
        AlgoBase.__init__(self)

    def fit(self, trainset):

        # Here again: call base method before doing anything.
        AlgoBase.fit(self, trainset)

        # Compute the average rating. We might as well use the
        # trainset.global_mean attribute ;)
        self.the_mean = np.mean([r for (_, _, r) in
                                 self.trainset.all_ratings()])

        return self

    def estimate(self, u, i):

        return self.the_mean


class MeanofMeans(AlgoBase):
    def __init__(self):

    # Always call base method before doing anything.
        AlgoBase.__init__(self)


    def fit(self, trainset):

        # Here again: call base method before doing anything.
        AlgoBase.fit(self, trainset)

        users = np.array([u for (u, _, _) in self.trainset.all_ratings()])
        items = np.array([i for (_, i, _) in self.trainset.all_ratings()])
        ratings = np.array([r for (_, _, r) in self.trainset.all_ratings()])

        user_means,item_means = {},{}
        for user in np.unique(users):
            user_means[user] = ratings[users==user].mean()
        for item in np.unique(items):
            item_means[item] = ratings[items==item].mean()

        self.global_mean = ratings.mean()
        self.user_means = user_means
        self.item_means = item_means

    def estimate(self, u, i):
        """
        return the mean of means estimate
        """

        if u not in self.user_means:
            return(np.mean([self.global_mean,
                            self.item_means[i]]))

        if i not in self.item_means:
            return(np.mean([self.global_mean,
                            self.user_means[u]]))

        return(np.mean([self.global_mean,
                        self.user_means[u],
                        self.item_means[i]]))

def get_mean_errors(cross_val_dict, rmse_key, mae_key):
    rmse = cross_val_dict[rmse_key].mean()
    mae = cross_val_dict[mae_key].mean()
    return rmse, mae

if __name__ == "__main__":

    df = pd.read_csv('../data/ml-latest-small/ratings.csv').drop(columns='timestamp')
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)
    
    print("\nGlobal Mean...")
    algo = GlobalMean()
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
    
    print("\nMeanOfMeans...")
    algo = MeanofMeans()
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
  
    a = cross_validate(GlobalMean(), data, measures=['RMSE', 'MAE'], cv=5)
    global_rmse, global_mae = get_mean_errors(a, 'test_rmse', 'test_mae')
    print('Mean RMSE: {}'.format(global_rmse))

    b = cross_validate(MeanofMeans(), data, measures=['RMSE', 'MAE'], cv=5)
    mom_rmse, mom_mae = get_mean_errors(b, 'test_rmse', 'test_mae')
    print('Mean RMSE: {}'.format(mom_rmse))