# Recommend a good joke.

Today you are going to have a little friendly competition with your classmates. 
You are going to building a recommendation system based off data from the 
[Jester Dataset](http://eigentaste.berkeley.edu/dataset/). It includes user 
ratings of over 100 jokes.

The joke data are in `data/jokes.dat`. The users'
ratings have been broken into a training and test set for you, with the training 
data in `data/training_ratings.csv`. Your goal is to build a recommendation system 
and to suggest jokes to users! Your score will be measured based off of how well 
you predict the top-rated jokes for the users' ratings in our test set. 

Note that we will be using [GraphLab](https://dato.com/) to build our 
recommendation system. If you don't already have it installed, follow the 
directions in [GraphLab_setup.md](GraphLab_setup.md).

To make sure that you have it set up correctly, run `code/rec_runner.py`. If it 
completes without error, you are good to go! Note that `code/rec_runner.py` 
outputs a _properly formatted_ file of recommendations for you! I suggest 
using this file as a base and building off of it as you work through the day. 

Next, make sure that you are able to post your score to slack. To begin, you'll
need to pip install the `performortron` library: 

```bash 
pip install git+https://github.com/zipfian/performotron.git --upgrade
```

After that, you should be able to use the `code/slack_poster.py` file to 
post your score to slack. The `code/slack_poster.py` file takes a _properly 
formatted_ file of recommendations (see `data/sample_submission.csv` for an 
example) and reports your score to Slack. Use the URL in `code/config.yaml` for 
the URL that `slack_poster` will prompt you for, and use a gschool channel to 
post results to, **prefacing the channel with a `#` when you are promted 
(i.e. #dsi)**. Test it out with the following command:
    
```bash
python code/slack_poster.py data/sample_submission.csv
```

See if you can get the best score! 

# Evaluation

## Score

For each user, our scoring metric will select the 5% of movies you thought would be most highly rated by that user. It then looks at the actual ratings (in the test data) that the user gave those movies.  Your score is the average of those ratings.

Thus, for an algorithm to score well, it only needs to identify which movies a user is likely to rate most highly (so the absolute accuracy of your ratings is less important than the rank ordering).

As mentioned above, your submission should be in the same format as the sample 
submission file, and the only thing that will be changed is the ratings column. 
Use `code/rec_runner.py` as a starting point, as it has a function to create 
correctly formatted submission files.
