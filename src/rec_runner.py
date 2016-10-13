import pandas as pd
import graphlab as gl

def manip_sample_sub_format(sample_sub):
    """
    Return SFrame based on sample sub, with movid id pulled into separate format for consistency
    with the data used for model fitting.
    """
    sample_sub['movie'] = sample_sub.id.apply(lambda x: int(x.split('_')[1]))
    for_prediction = gl.SFrame(sample_sub)
    return for_prediction


if __name__ == "__main__":
    sample_sub_fname = "data/sample_submission.csv"
    ratings_data_fname = "data/training_ratings.csv"
    output_fname = "data/test_ratings.csv"

    ratings = gl.SFrame(ratings_data_fname)
    sample_sub = pd.read_csv(sample_sub_fname)
    for_prediction = manip_sample_sub_format(sample_sub)
    rec_engine = gl.factorization_recommender.create(   observation_data=ratings, 
                                                        user_id="user", 
                                                        item_id="movie", 
                                                        target='rating',
                                                        num_factors=4,
                                                        solver='auto')
    
    sample_sub.rating = rec_engine.predict(for_prediction)
    sample_sub.drop('movie', inplace=True, axis=1)
    sample_sub.to_csv(output_fname, index=False)
