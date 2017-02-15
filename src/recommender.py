import logging
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix

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

        utility_lil = lil_matrix((max(self.user_ids)+1,max(self.item_ids)+1))

        for index, row in ratings.iterrows():
            _user = row['user']
            _item = row['movie']
            utility_lil[_user,_item] = row['rating']

        self.utility = csr_matrix(utility_lil)

        self.logger.debug("finishing fit")
        return(self)  # we return self to use .predict() on it


    def predict(self, requests):
        """On a given dataframe, predict the ratings.
        Returns the ratings df with an added 'rating' column. (???)
        """
        self.logger.debug("starting predict")

        self.logger.debug("request count: {}".format(requests.shape[0]))

        # just relying on luck for now...
        #output_ratings = np.zeros(requests.shape[0])

        #for index, row in requests.iterrows():
        #    output_ratings[index] = 0

        output_ratings = np.random.choice(range(1, 5), requests.shape[0])

        self.logger.debug("result shape: {}".format(output_ratings.shape))
        self.logger.debug("finishing predict")
        return(output_ratings)

    def similarity_uu(self, user_i, user_j):
        pass

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.critical('you should use run.py instead')
