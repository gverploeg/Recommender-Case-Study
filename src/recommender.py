import logging
import numpy as np

class Recommender():
    def __init__(self, **kwargs):
        """
        blabla
        """
        self.logger = logging.getLogger()
        self.user_field = kwargs.get('user_id', 'user')
        self.item_field = kwargs.get('item_id', 'movie')
        self.target_field = kwargs.get('target', 'rating')


    def fit(self, ratings):
        """Fits the recommender on the given ratings
        Returns a model (an object that has a predict function)
        """
        self.logger.debug("starting fit")

        # ...

        self.logger.debug("finishing fit")
        return(self)  # we return self to use .predict() on it


    def predict(self, ratings):
        """On a given dataframe, predict the ratings.
        Returns the ratings df with an added 'rating' column. (???)
        """
        self.logger.debug("starting predict")

        # just relying on luck...
        ratings[self.target_field] = np.random.choice(range(1, 5), ratings.shape[0])

        self.logger.debug("finishing predict")
        return(ratings)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.critical('you should use rec_runner.py instead')
