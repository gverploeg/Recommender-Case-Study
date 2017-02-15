import logging
import numpy as np
from scipy.sparse import lil_matrix

class MovieRecommender():
    def __init__(self):
        """
        blabla
        """
        # if you want to use this...
        self.logger = logging.getLogger()


    def fit(self, ratings):
        """Fits the recommender on the given ratings
        Returns a model (an object that has a predict function)
        """
        self.logger.debug("starting fit")

        self.logger.debug("shape of ratings: {}".format(ratings.shape))

        self.user_ids = set(ratings['user'])
        self.item_ids = set(ratings['movie'])

        self.logger.debug("users: {} // items: {}".format(max(self.user_ids),max(self.item_ids)))

        self.utility = lil_matrix((max(self.user_ids)+1,max(self.item_ids)+1))

        for index, row in ratings.iterrows():
            _user = row['user']
            _item = row['movie']
            self.utility[_user,_item] = row['rating']

        self.logger.debug("finishing fit")        
        return(self)  # we return self to use .predict() on it


    def predict(self, ratings):
        """On a given dataframe, predict the ratings.
        Returns the ratings df with an added 'rating' column. (???)
        """
        self.logger.debug("starting predict")

        # just relying on luck for now...
        ratings['rating'] = np.random.choice(range(1, 5), ratings.shape[0])

        self.logger.debug("finishing predict")
        return(ratings)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.critical('you should use run.py instead')
