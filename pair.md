# Tell Users Which Movies to Watch

This contest gives you a new and larger version of the MovieLens dataset.  It includes more movies and more users, but the most recent 50% of the ratings have been removed from the version you receive to create the test dataset.

The data are in `data/movies.dat` and `data/ratings.dat`.

Note that the submission data includes an id column that is in the form `<user_number>_<movie_number>`.

The file `code/rec_runner.py` takes a _properly formatted_ file of recommendations (see `data/sample_submission.csv`) for an example and reports your score to Slack. It can be run with the following command:

    python code/rec_runner.py data/YOUR_SUBMISSION.csv

This will allow you to see how your recommendations compare to your peers! See if you can get the best!

# Evaluation

## Score

For each user, our scoring metric will select the 5% of movies you thought would be most highly rated by that user. It then looks at the actual ratings (in the test data) that the user gave those movie.  Your score is the average of those ratings.

Thus, for an algorithm to score well, it only needs to identify which movies a user is likely to rate most highly (so the absolute accuracy of your ratings is less important than the rank ordering).

Your submission should be in the same format as the sample submission file, and the only thing that will be changed is the ratings column. Use rec_runner.py as a starting point, and it has a function to create correctly formatted submission files.
