# Building a Better Tinder

![](https://pbs.twimg.com/media/B9Wo6s1CcAIiFWY.jpg:large)

Today's pair exercise is going to give us experience applying the theory of recommenders to a real world product... Dating!

In this sprint, we will try to build a better Tinder by incorporating all of the theory we learned yesterday to rank and suggest users to each other.  In addition to evaluating and engineering an optimal recommender, we will be building a larger data pipeline to simulate an example of putting a model into production.

## The Data

We will be using [this](http://www.occamslab.com/petricek/data/) data set of user ratings of each other.  The ratings data has been transformed from a scale of 1-10 into { 0 | 1 }: 0 if you have never seen a profile, and 1 if you have clicked on a users' picture.

You can find this transformed dataset in `data/ratings.csv`.  There is also a mapping to the users gender in `data/gender.csv`.

## Getting Started

To start, we are going to build a basic collaborative filter to create a baseline.  And since there are quite a few ratings (17,359,346 to be exact), we will be using [Dato](https://dato.com/) (formerly Graphlab) to build our recommendation engine.

Our goal throughout is to determine the next series of profiles to show a given user. Or more explicitly, for user __X__, what are the __N__ profiles that user __X__ is most likely to swipe right (like) on.

1. To start, let us explore the data. What is the distribution of ratings (how many -1 vs. 1)?

2. Create a histogram of the number of ratings each user has made.  On average how many ratings does a user make?  Will this cause issues for your recommender?

3. 
Who are the top 20 users you

 ## Evaluation (Pt. 1)

 In the beginning, (data) scientists an engineers applied the same methodology they used for prediction to recommendations: __accuracy__.

 Models for recommendation were evaluated using a lot of the same methodology as classifiers/regression... but the industry quickly realized that recommenders are not simply predictors of user ratings.

1. Let us start with this naive evaluation strategy.  Using a holdout set of 20% vs. 80%, use the `[evaluate]()` functionality of Dato to compute the RMSE for your recommender.

2. We learned about different distance metrics yesterday.  Compare the performance of Jaccard vs. Cosine vs. Pearson.

3. Why might/might not Jaccard be good for the given preference data we have?

 Normalization:
* subtract bias from rating matrix (both for rating and users)


 ## Feature Engineering

 Before we start engineering our features, let us think critically about the data we have.

1. Are these ratings/preferences implicit or explicit?

2. Name 2 differences between implicit vs. explicit data.  Which one is a stronger signal?
 
 Assume that we have control over our data/application.  As a next step the engineers have changed the application from a pinterest like browsing experience to a Tinder [like](https://vine.co/v/OP7jzumxuhd) swipe left or right experience.  And the data collection has gone from simply "have you seen this user or not" to: have you swiped left or right on this user.

3. Transform the initial data (`data/ratings.csv`) into this new swipe left or right preference by mapping any rating of __6-10 -> 1__ (swipe right) and __1-5 -> -1__ (swipe left).

4. Re-evaluate your recommender with this new featurization of your data.  Does it perform better than the binary preferences?

 And the last iteration on transforming the user preferences is to use the original 1-10 rating (assume the engineers have built into the application a way to give a scaled rating of a user)

5. Using the 1-10 rating data, evaluate your recommender and compare its performance to the other two preference types.  Which performed the best?

 ## Evaluation (Pt. 2)

Cross validating a recommender:
* treat each cell as a label
* selective block out ratings (20% for each user)

A/B test a recommender in production
* How many users will you have to give recommendations to assuming you want 80% power and 95% confidence with a lift of 5% more engagement time?
* How long will it take assuming you are EverPix?

How to qualify your recommendation: You got recommended this movie because...

 ## Productionizing

 ## Troubleshooting

 One of the canonical problems with building a recommendation engine is the [cold-start problem](https://www.linkedin.com/pulse/20130429011005-50510-the-cold-start-problem).

 One potential solution is to use other information around your given domain, often in the form of "content" based data such as properties (size, shape, cost) or features (genre, category, etc.) of given products.

 We will run into a potential more sinister version of this cold start problem since the only prior information we have on a user before they make any ratings is his/her gender.

1. How would you determine an order of profiles to show for a user who has just joined?  What are the next 20 profiles you would show for user xxxx?

2. Why might you want to intentionally not rank the profiles to show a given user by those which are most likely to be swiped right on?

