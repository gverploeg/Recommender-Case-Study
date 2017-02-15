import sys
import logging
import argparse
from recommender import Recommender     # the class you have to develop
import pandas as pd


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", help="path to training ratings file (to fit)")
    parser.add_argument("--requests", help="path to the input requests (to predict)")
    parser.add_argument("--output", help="output file (where predictions are stored)")
    parser.add_argument('--silent', action='store_true', help="deactivate debug output")

    args = parser.parse_args()

    if args.silent:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()


    path_train_ = args.train if args.train else "data/training_ratings.csv"
    logger.debug("using training ratings from {}".format(path_train_))

    path_requests_ = args.requests if args.requests else "data/requests.csv"
    logger.debug("using requests from {}".format(path_requests_))

    path_output_ = args.output if args.output else "data/predicted_ratings.csv"
    logger.debug("using output as {}".format(path_output_))

    # REQUESTS: reading from input file into pandas
    request_data = pd.read_csv(path_requests_)

    # TRAINING: reading from input file into pandas
    train_data = pd.read_csv(path_train_)

    # Creating an instance of your recommender with the right parameters
    reco_instance = Recommender(user_id="user",
                                item_id="movie",
                                target='rating')

    model = reco_instance.fit(train_data)
    result_data = model.predict(request_data)

    if 'rating' not in result_data.columns:
        logger.critical("column 'rating' does not exist in the df returned by recommender")
        sys.exit(-1)

    result_data.to_csv(path_output_, index=False)
