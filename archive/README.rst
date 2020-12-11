
Recommender Case Study
=======================

Students will use collaborative filtering and matrix factorization in Spark or Surprise in this case study.


Team organization
---------------------

There are three aims of the following case study:

  1. **Improve your big data skills** by including as part of your solution a working recommender written in Spark.
  2. **Demonstrate your knowledge of recommendation systems** by using the library **Surprise** to tweak and customize different algorithms
  3. **Practice you communication** by presenting to a non-technical audience

Spark and the big data solution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are two useful links for the Spark part.

  * https://spark.apache.org/docs/latest/ml-collaborative-filtering.html
  * https://www.codementor.io/jadianes/building-a-recommender-with-apache-spark-python-example-app-part1-du1083qbw

The first link is the official documentation.  The second is a
solution posted in a blog and although it uses MLlib instead of ML it
is still a useful resource.  ML is the more stable library and it is preferred to MLLib (if possible).

Surprise
^^^^^^^^^^^^

Surprise has a version of the data built in to it.

  * http://surpriselib.com/

And the documentation is pretty good.


The Case Study
--------------------------------------

You and a team of talented data scientists are working for the
company, **Movies-Legit**, who has used a production recommenders for
many years now.  The recommender provides a significant revenue stream
so your managers are heisitent to touch it.  The issue is that these
systems have been around a long time and your head of data science has
asked you and your team members to explore new solutions.

The solution that has been around for so long is called the **Mean of
Means**.  We see that some users like to rate things highly---others
simply do not.  Some items are just better or worse.  We can capture
these general trends through per-user and per-item rating means. We
also incorporate the global mean to smooth things out a bit. So if we
see a missing value in cell $R_{ij}$, we'll average the global
mean with the mean of $U_i$ and the mean of $V_j$ and use
that value to fill it in.

We would like you to use this as a baseline when making your
comparisons.  The basic code showing you how this is done is provided
for you in `src/baselines.py`.
   
At the end of the day you are to present your solution to the bosses
and the entire product team.  You can assume that they have little to no
depth of knowledge in statistics and big data technologies.

The main goal here is to improve the RMSE, however, another equally
important goal is to present your model and the details of your
explorations in a clear, but technically sound manner.  *You need to
convince us that you understand the tools you are using AND that it is
a better way forward.* After all we are making a lot of money with
*mean of means* and it is a major risk to swap it out with anything else.

We would also like you to include some discussion about how you would
move from prototype to production.

The data
--------------

MovieLens is a classical recommender dataset and your audience is already familiar with it.

There is a larger version of the dataset available from the link
below, but we do not expect a production ready recommender in only a
days time so do not worry too much about scale for now.  You will find
the smaller version of the data as part of this repo.


  * https://grouplens.org/datasets/movielens

    
Helpful hints
------------------

  * A challenge with the Spark solution can be to implement a *mean of means* baseline
  * Surprise can be challenging to shape into what you might want, but it has a lot builtin
  * Make sure you show an example of a prediction
  * **The numeric results are not as important here as how well you communicate what you have done**  
  * Finally, the 'bosses' are not real keen thinking too hard about
    RMSE or MAE.  You might be able to explain it to them, but if you
    report it as percent improvement over mean-of means they are more
    likely to listen.
    
Good luck!
