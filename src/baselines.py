#!/usr/bin/env python

"""
http://surprise.readthedocs.io/en/stable/building_custom_algo.html
"""

import sys
import numpy as np
import pandas as pd 
from surprise import AlgoBase, Dataset, Reader
from surprise.model_selection.validation import cross_validate

'''classes used by company for their model'''
class GlobalMean(AlgoBase):
    '''just uses the ratings mean to fill in empty spaces in matrix'''
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
    '''uses user, movie and rating information to get means for all three vectors to fill in matrix'''
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

#our function, to calculate the error values (ended up not using this, but the cross_validate function from surprise
# returns a dictionary of the values that are in our final dataframe table)
def get_mean_errors(cross_val_dict, rmse_key, mae_key):
    rmse = cross_val_dict[rmse_key].mean()
    mae = cross_val_dict[mae_key].mean()
    return rmse, mae

if __name__ == "__main__":
    #pandas dataframe of the ratings csv
    df = pd.read_csv('../data/ml-latest-small/ratings.csv').drop(columns='timestamp')
    #Reader class from Surprise, you have to tell it the scale that will be in the rating column
    reader = Reader(rating_scale=(0.5, 5))
    #use the reader object we made above in loading the dataframe into a data for use; Dataset is a class in surprise so that is how
    #load your own dataframe in
    data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)
    
    print("\nGlobal Mean...")
    #need to make a variable be the global mean algorithm from above
    algo = GlobalMean()
    #use Surprise cross_validate with 5 folds to get back the rmse and mae measures. Verbose=True means you will see the printout
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    
    print("\nMeanOfMeans...")
    algo = MeanofMeans()
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
  
