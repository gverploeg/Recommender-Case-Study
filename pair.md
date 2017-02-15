# Objective: Tell Users Which Movies to Watch

Today you are going to have a little friendly competition with your classmates.
You are going to building a recommendation system based off data from the
[MovieLens dataset](http://grouplens.org/datasets/movielens/). It includes movie
information, user information, and the users' ratings. Your goal is to build a
recommendation system and to suggest movies to users!


## Training / Testing and scoring

The **movies data** and **user data** are in `data/movies.dat` and `data/users.dat`. The users'
ratings have been broken into a training and test set for you (the split has been done by keeping the most recent 50% of the ratings for the testing set).

The ratings from the **training data** can be found in `data/training_ratings.csv`.

You are provided a **request** file in `data/requests.csv`. It contains a list of `user,movie,id` for which you need to predict the (missing) `rating` column. Your **score** will be measured based on how well you predict the ratings for the users' ratings compared to our test set.

The ratings for the **testing data** can be found in `data/dont_use.csv`... as indicated by the filename, you SHOULD NOT USE this file to train your model. This would be considered as cheating.


## How to implement your recommender

The file `src/recommender.py` is your main template for creating your recommender. You can work from this file and implement whatever strategy you think is best. You need to implement both the `.fit()` and the `.predict()` methods.


## How to run your recommender

`src/run.py` has been prepared for your convenience (doesn't need modification). By executing it you create an instance of your `Recommender`, feeds it with the training data and outputs the results in a file.

It outputs a _properly formatted_ file of recommendations for you! I suggest using this file as a base and building off of it as you work through the day.

  Here's how to use this script:
  ```bash
  usage: run.py [-h] [--train TRAIN] [--requests REQUESTS] [--output OUTPUT]
                [--silent]

  optional arguments:
    -h, --help           show this help message and exit
    --train TRAIN        path to training ratings file (to fit)
    --requests REQUESTS  path to the input requests (to predict)
    --output OUTPUT      output file (where predictions are stored)
    --silent             deactivate debug output
  ```

**You need to** specify your prediction output file `--output` option.


## How to submit your score to Slack

`src/submit.py` is the script you'll use to submit your results. It reads your submission from a file and computes your score against the testing test.

  Here's how to use this script:
  ```bash
  usage: submit.py [-h] --prediction PREDICTION [--score] [--submit] [--silent]

  optional arguments:
    -h, --help            show this help message and exit
    --prediction PREDICTION
                          prediction file to submit
    --score               display score
    --submit              submits result on slack
    --silent              deactivate debug output
  ```

**You need to** specify your prediction file (the one produced by `src/run.py`) using the `--prediction` option.

**You need to** explicitely specify `--submit` to submit to slack.

You can use `--score` to display the score (not submitting).


## TODO: test your installation

Before doing anything, make sure that you are able to post your score to slack. To begin, you'll need to pip install the `performortron` library:

```bash
pip install git+https://github.com/zipfian/performotron.git --upgrade
```

After that, you should be able to use the `src/submit.py` file to post your score to slack.

In a terminal, use

```bash
python src/submit.py --prediction data/sample_submission.csv --score --submit
```

This will take a _properly formatted_ file of recommendations (see `data/sample_submission.csv` for an
example). This should output the score `3.56090572255` (random ratings) and submit it to slack from "Team Anonymous".

Modify the file `conf/config.yaml` for setting up your team's name and test that again.

the URL that `slack_poster` will prompt you for, and use a gschool channel to
post results to, **prefacing the channel with a `#` when you are promted
(i.e. #dsi)**.


## Evaluation: how the score is computed

For each user, our scoring metric will select the 5% of movies you thought would be most highly rated by that user. It then looks at the actual ratings (in the test data) that the user gave those movies.  Your score is the average of those ratings.

Thus, for an algorithm to score well, it only needs to identify which movies a user is likely to rate most highly (so the absolute accuracy of your ratings is less important than the rank ordering).

As mentioned above, your submission should be in the same format as the sample
submission file, and the only thing that will be changed is the ratings column.
Use `src/run.py` as a starting point, as it has a function to create
correctly formatted submission files.
