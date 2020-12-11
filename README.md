<div align="center">  
<header>
    <h1>Movies-Legit<br>
    New Movie Recommender Pitch</h1>
  </header>
<div align='left'>  

![](images/movie_banner.jpg)
[source](https://www.facebook.com/MRPJD/photos/a.113642393607538/116536716651439)  

## Table of Contents
1. [Background](#background)
2. [Data](#data)
3. [New Recommender](#new-recommender)
4. [Analysis and Business Advice](#analysis-and-business-advice)

## Background

Our data science team has been tasked with proposing a new movie recommender platform for **Movies-Legit**.   

Currently, the company uses their **Mean of Means** solution, which captures the general per-user and per-item trends of rating movies. If there are any missing ratings, the model averages the global mean along with the mean of the user and item ratings to fill in the value. 

## Data  

### Initial Data
The data used to evaluate the current **Mean of Means** model, as well as build our new recommender model is from the [MovieLens dataset](https://grouplens.org/datasets/movielens/). The small sample dataset we are using consists of four csv files:
-  ```movies.csv```: 193,609 movies listed with a unique ```movieId```, their title and the genres to which the movie belongs
-  ```ratings.csv```: Ratings ranging between 0.5 to 5.0 from 610 users with unique ```userId``` for various movies linked by their unique ```movieId```
-  ```tags.csv```: User identified tags for each movie specified by the unique ```userId``` and ```movieId```
-  ```links.csv```: ??

### Merged Data: PySpark, SQL & Pandas


## New Recommender Model


## Analysis and Business Advice