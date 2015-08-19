import pandas as pd
import graphlab as gl


def manip_sample_sub_format(sample_sub):
    """
    Return SFrame based on sample sub, with movid id pulled into separate
    format for consistency with the data used for model fitting.
    """
    for_pred = gl.SFrame(sample_sub)
    for_pred['movie'] = sample_sub.id.apply(lambda x: int(x.split('_')[1]))
    return for_pred


if __name__ == "__main__":
    sample_sub_fname = "data/sample_submission.csv"
    ratings_data_fname = "data/training_ratings_for_kaggle_comp.csv"
    output_fname = "test_submission.csv"

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
    sample_sub.to_csv(output_fname, index=False)
