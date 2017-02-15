import sys
import logging
import argparse
from recommender import Recommender     # the class you have to develop
import pandas as pd

from performotron import Comparer

class RecComparer(Comparer):
    def score(self, predictions):
        """Look at 5% of most highly predicted movies for each user.
        Return the average actual rating of those movies.
        """
        #sample = pd.read_csv('data/sample_submission.csv')

        df = pd.concat([#sample,
                        predictions,
                        self.target], axis=1)

        g = df.groupby('user')

        top_5 = g.rating.transform(
            lambda x: x >= x.quantile(.95)
        )

        return self.target[top_5==1].mean()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prediction", required=True, help="prediction file to submit")
    parser.add_argument('--score', action='store_true', help="display score")
    parser.add_argument('--submit', action='store_true', help="submits result on slack")
    parser.add_argument('--silent', action='store_true', help="deactivate debug output")
    args = parser.parse_args()

    if args.silent:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()


    path_prediction_ = args.prediction if args.prediction else "data/sample_submission.csv"
    logger.debug("using predictions from {}".format(path_prediction_))
    prediction_data = pd.read_csv(path_prediction_)

    if prediction_data.shape[0] != 500109:
        error_msg_ = " ".join(["Your matrix of predictions is the wrong size.",
        "It should provide ratings",
        " for 500109 entries (yours={}}).".format(prediction_data.shape[0])])
        logger.critical(error_msg_)
        sys.exit(-1)


    test_data = pd.read_csv('data/dont_use.csv')
    test_data.rating.name='test_rating'
    rc = RecComparer(test_data.rating, config_file='conf/config.yaml')


    if args.score:
	    print("score={}".format(rc.score(prediction_data)))

    if args.submit:
        logger.critical("slack not configured yet")
        sys.exit(-1)
        #rc.report_to_slack(sample_sub)
