import sys
import logging
import argparse
import pandas as pd

def compute_score(predictions, actual):
    """Look at 5% of most highly predicted movies for each user.
    Return the average actual rating of those movies.
    """
    #sample = pd.read_csv('data/sample_submission.csv')

    df = pd.concat([predictions, actual.actualrating], axis=1)

    # for each user
    g = df.groupby('user')

    # detect the top_5 movies as predicted by your algorithm
    top_5 = g.rating.transform(
        lambda x: x >= x.quantile(.95)
    )

    # return the mean of the actual score on those
    return actual.actualrating[top_5==1].mean()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--silent', action='store_true', help="deactivate debug output")
    parser.add_argument("predfile", nargs=1, help="prediction file to submit")
    parser.add_argument("groundtruthfile", nargs=1, help="actual ratings")

    args = parser.parse_args()

    if args.silent:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)
    else:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
    logger = logging.getLogger()

    logger.debug("using predictions from {}".format(args.predfile[0]))
    prediction_data = pd.read_csv(args.predfile[0])

    logger.debug("using groundtruth from {}".format(args.groundtruthfile[0]))
    actual_data = pd.read_csv(args.groundtruthfile[0])

    if prediction_data.shape[0] != actual_data.shape[0]:
        error_msg_ = " ".join(["Your matrix of predictions is the wrong size.",
        "It should provide ratings for {} entries (yours={}}).".format(actual_data.shape[0],prediction_data.shape[0])])
        logger.critical(error_msg_)
        sys.exit(-1)

    if prediction_data.shape[0] != 500109:
        logger.warn('YOUR PREDICTION DOESNT HAVE THE RIGHT FORMAT FOR SUBMITTING.')

    logger.debug("score={}".format(compute_score(prediction_data, actual_data)))
