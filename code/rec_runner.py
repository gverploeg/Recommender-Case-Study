import pandas as pd
import graphlab as gl
from performotron import Comparer

def manip_sample_sub_format(sample_sub):
    """
    Return SFrame based on sample sub, with movid id pulled into separate
    format for consistency with the data used for model fitting.
    """
    for_pred = gl.SFrame(sample_sub)
    for_pred['movie'] = sample_sub.id.apply(lambda x: int(x.split('_')[1]))
    return for_pred

class RecComparer(Comparer):
    def score(self, predictions):
        """Look at 5% of most highly predicted movies for each movie.
        Return the average actual rating of those movies.
        """
        #sample = pd.read_csv('data/sample_submission.csv')
        
        df = pd.concat([#sample,
                        predictions,
                        self.target])
        g = df.groupby('user')
        
        top_5 = g.rating.transform(
            lambda x: x>=x.quantile(.95)
        )

        return self.target[top_5].mean()

if __name__ == "__main__":
    sample_sub_fname = "data/sample_submission.csv"
    ratings_data_fname = "data/training_ratings_for_kaggle_comp.csv"
    output_fname = "test_submission.csv"

    test=pd.read_csv('data/dont_use.csv')
    rc = RecComparer(test.rating, config_file='code/config.yaml')
    
    ratings = gl.SFrame(ratings_data_fname)
    sample_sub = pd.read_csv(sample_sub_fname)
    for_prediction = manip_sample_sub_format(sample_sub)
    rec_engine = gl.factorization_recommender.create(observation_data=ratings,
                                                     user_id="user",
                                                     item_id="movie",
                                                     target='rating',
                                                     num_factors=4,
                                                     solver='auto')

    sample_sub.rating = rec_engine.predict(for_prediction)

    rc.report_to_slack(sample_sub)
    
    #sample_sub.to_csv(output_fname, index=False)


