## Music Recommendations

For today's sprint, we will be giving music recommendations for a given set of users.  The dataset is on the Mac Mini's already in `~/datasets/lastfm-dataset-1k` folder (or on theTimeCapsul). It contains the complete listening history of ~1000 users from lastfm.com.  A description can be found in the data folder (or from the original link [here](http://www.dtic.upf.edu/~ocelma/MusicRecommendationDataset/lastfm-1K.html)).

We will be using a new library called [GraphLab](http://graphlab.com/learn/index.html) to perform our analysis.  GraphLab has one of the more advanced recommendation algorithms built in (in addition to graph processing functionality).  GraphLab's main data structure is called the [SFrame](http://graphlab.com/learn/notebooks/introduction_to_sframes.html): a disk-backed DataFrame.  It has an API very similar to pandas and should feel very familiar to you.  The main difference is that it stores it's SFrames on disk (if they do not fit in memory).

The data file we will be using is a bit large (~2 GB) but both pandas and GraphLab should be able to handle it.  Since GraphLab inter-operates with pandas so nicely we can jump between the two if we so please.

Since GraphLab makes it so [easy](http://graphlab.com/learn/notebooks/five_line_recommender.html) to make a recommendation, in this sprint we will focus on some real world challenges with Recommenders, mainly defining preferences and features.

Recall that we use preference data (rating, reviews, etc.) to create our feature matrix.  Often times explicit preferences are used directly as features but in this sprint we will explore some other techniques, and always remember: __[Product is more important than math](http://blog.mortardata.com/post/58246541129/recommender-tips-product-is-more-important-than-math)__

### EDA

__Tutorials: [http://graphlab.com/learn/index.html](http://graphlab.com/learn/index.html)__

1. Explore the data files.  To start load them into a GraphLab SFrame.

2. We will do some exploratory analysis in pandas first.  How many users are there?  How many artists are there? How many songs are there?

3. What is user 666's favorite song (and how absolutely heavy metal is it)?  What are user 333's top 10 favorite songs?

### Recommend

Now that we have played around with the data it is time to begin recommending.  If you recall when we built our own recommender we had a very sparse matrix.  If we represent this as a 'dense' matrix it results in us storing a lot of 0's (which take up just as much memory as 1's and 2's and...).  The [recommender](http://graphlab.com/products/create/docs/graphlab.toolkits.recommender.html) toolkit in GraphLab actually operates on sparse data directly (and SFrames natively represent sparse data), we store it in a similar many to our bag of words from the Naive Bayes sprint: each row of our SFrame represents a (user, item, rating) vector.  There are many duplicate rows for each user.

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>song</th>
      <th>user</th>
      <th>Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>                                      Angelene</td>
      <td> user_000901</td>
      <td> 4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>                                        Animal</td>
      <td> user_000477</td>
      <td> 1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>                                           Run</td>
      <td> user_000582</td>
      <td> 4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>          Silmarillia 2007 (Leon Bolier Remix)</td>
      <td> user_000746</td>
      <td> 2</td>
    </tr>
    <tr>
      <th>4</th>
      <td> Hide U (John Creamer &amp; Stephane K Remix Edit)</td>
      <td> user_000362</td>
      <td> 4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>                                If It'S In You</td>
      <td> user_000829</td>
      <td> 4</td>
    </tr>
    <tr>
      <th>6</th>
      <td>               All Out Of Time, All Into Space</td>
      <td> user_000915</td>
      <td> 2</td>
    </tr>
    <tr>
      <th>7</th>
      <td>                   Silent Tomorrow (Dark Edit)</td>
      <td> user_000745</td>
      <td> 1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>                                        Blonde</td>
      <td> user_000617</td>
      <td> 4</td>
    </tr>
    <tr>
      <th>9</th>
      <td>                     Daniel, Where'S The Boat?</td>
      <td> user_000056</td>
      <td> 1</td>
    </tr>
     <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

1. Before we can start recommending we need to create our feature matrix. To create our feature matrix, we will convert our implicit user preferences (song listens) into something meaningful.  Create a feature matrix where each row represents a (user, song, listen count) triplet (i.e. 3 columns).

3. When we try to compute our recommendations, we will blow up our memory unless we take a subset of the data.  Subset your SFrame such that you only include (user, song) pairs with at least 25 listens.

2. The simplest model might be to just predict the global mean.  Using the [recommender](http://graphlab.com/products/create/docs/graphlab.toolkits.recommender.html) toolkit, create an ItemMeansModel.

### Evaluation

Recommenders are notoriously hard to evaluate. GraphLab makes it pretty effortless to run a test-train split cross validation on your data.

1. Using GraphLab, create a test-train split (`random_split` or `random_split_by_user`) and evaluate how your basic recommender performs with [RMSE](http://graphlab.com/products/create/docs/graphlab.toolkits.evaluation.html).

2. Since some users may listen to music much more in general, we want to normalize the counts.  Normalize the listen counts for each user by the total song plays by that user.

3. Create a new recommender using this new normalized feature matrix and [compare](http://graphlab.com/products/create/docs/generated/graphlab.recommender.compare_models.html#graphlab.recommender.compare_models) its performance to the un-normalized feature matrix.  Which performs better?  And by how much?

### Collaboration

Now you might be asking yourself why we created such a simple model, we hand-coded a Collaborative filter after all!  The ItemMeansModel will serve as our baseline, remember:

![data science pyramid](images/data_science_pyramid.jpg)

1. Create a [basic collaborative filter](http://graphlab.com/learn/notebooks/five_line_recommender.html) on the listening data. Use the [item-similarity model](http://graphlab.com/products/create/docs/generated/graphlab.recommender.ItemSimilarityModel.html#graphlab.recommender.ItemSimilarityModel) with cosine distance as the `similarity_type`.  __NOTE: This is an item-item collaborative filter__

2. Compare it's performance to your baseline.

3. Use your model to generate the top 5 recommendations for each user.  Do this for the baseline as well as the collaborative filter.

### More models!

GraphLab has quite an extensive choice of recommendation models and they all can be seamlessly compared.

1. Create a [Matrix Factorization model](http://graphlab.com/products/create/docs/generated/graphlab.recommender.MatrixFactorizationModel.html#graphlab.recommender.MatrixFactorizationModel) and compare it's performance to the item-based collaborative filter.  Which performs better?

3. As with most Machine Learning models, there are parameters to tune for our recommender.  Vary the regularization parameter on the matrix factorization model and compare based on RMSE.  What is the ideal value for the regularization parameter?

4. Do the same for the number of factors parameter.  What is the ideal number of factors for our data?

5. Compare the matrix factorization model to a [Regression](http://graphlab.com/products/create/docs/generated/graphlab.recommender.LinearRegressionModel.html#graphlab.recommender.LinearRegressionModel) model.  Which gets better performance?

### Similarity

7. For a given user looking at a song, also recommend similar songs.  GraphLab doesn't give us similar songs/items but we can use our plain old distance metric to calculate it.  Convert the SFrame to a DataFrame and pivot it such that each column is a user and each row is a song.  

8. Using scipy's [pdist](http://docs.scipy.org/doc/scipy-0.13.0/reference/generated/scipy.spatial.distance.pdist.html) compute a similarity matrix.

9. For a given song you can compute the K most similar songs.  Try this for a few of your favorite songs and see if the results make any sense.

![](http://www.quickmeme.com/img/20/20ef0c9170bbfc7ae11915a9103af38d86285dc3f49d2d1723ebe36601217244.jpg)

## Extra Credit

Recommenders can be one of the most nuanced (and creative) model.  The dataset we are dealing with is very rich and the amount of information available on songs is mind boggling.

### Signals

We have drastically simplified the data we have been dealing with by just aggregating the user listens across all time.  Experiment with the following features:

* Most recently listened to song.
* Song with longest streak (i.e. most listens in a row)
* Most consistent song (i.e. smallest variance in time delta between listens)
* Monthly listens for each song
* Anything you can imagine!

### Content

As mentioned in lecture content based recommender have their own set of pros and cons.  Often the best recommendations combine the two approaches into a hybrid recommender.

Build a content based recommender using the [Million Song Dataset](http://labrosa.ee.columbia.edu/millionsong/) and [Echo Nest](http://developer.echonest.com/)

1. The dataset we have contain [MusicBrainz](https://musicbrainz.org/) ids.  To be able to use the MSD we need the associated Echo Nest song_id.  Using the [Echo Nest API](http://developer.echonest.com/forums/thread/816), find the corresponding `song id` for a given MusicBrainz id for every song in our dataset.

```
http://developer.echonest.com/api/v4/song/profile?api_key=XXX&id=musicbrainz:song:54753489-ee00-48bd-ad43-8c0f5c365bff
```

2. Now that we have enriched our data with identifiers to link our song to the MDS, we can use all of its rich [meta-data](http://labrosa.ee.columbia.edu/millionsong/pages/field-list) to create a content based recommender.  Create a new feature matrix for our content based song recommender.  Each row should be a song and each column should be a corresponding feature.  Do not feel you need to use all of the [fields](http://labrosa.ee.columbia.edu/millionsong/pages/field-list) from the MSD.

3. Create a content based recommender.  Combine this with our matrix factorization (or collaborative filter) based on the listen counts.  You can blend the models by assigning a weight to each of the predictions and even customize it on a user-by-user basis (depending on their preferences).

## References

### GraphLab

* [Getting Started with GraphLab Create](http://graphlab.com/learn/notebooks/getting_started_with_graphlab_create.html)
* [Five Line Recommender Explained](http://graphlab.com/learn/notebooks/five_line_recommender.html)
* [Building a Recommender with Ratings Data](http://graphlab.com/learn/notebooks/recsys_explicit_rating.html)
* [Basic Recommender Functionalities](http://graphlab.com/learn/notebooks/basic_recommender_functionalities.html)
* [Building a Recommender with Implicit data](http://graphlab.com/learn/notebooks/recsys_rank_10K_song.html)

### Mortar Data

* [Product is more important than math](http://blog.mortardata.com/post/58246541129/recommender-tips-product-is-more-important-than-math)
* [Building a Recommendation Engine](http://help.mortardata.com/data_apps/recommendation_engine/recommendation_engine_basics)
* [Improving Recommendations](http://help.mortardata.com/data_apps/recommendation_engine/interpret_results)