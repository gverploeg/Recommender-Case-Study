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
3. [New Recommender Models](#new-recommender-models)
4. [Analysis and Business Advice](#analysis-and-business-advice)

## Background

Our data science team has been tasked with proposing a new movie recommender platform for **Movies-Legit**.   

Currently, the company uses their **Mean of Means** solution, which captures the general per-user and per-item trends of rating movies. If there are any missing ratings, the model averages the global mean along with the mean of the user and item ratings to fill in the value.   



## Data  

### Initial Data
The data used to evaluate the current **Mean of Means** model, as well as build our new recommender model is from the [MovieLens dataset](https://grouplens.org/datasets/movielens/). The small sample dataset we are using consists of four csv files:
-  ```movies.csv```: 193,609 movies listed with a unique ```movieId```, their title and the genres to which the movie belongs--our small sample has about 9,700 movies
-  ```ratings.csv```: Ratings ranging between 0.5 to 5.0 from 610 users with unique ```userId``` for various movies linked by their unique ```movieId```
-  ```tags.csv```: User identified tags for each movie specified by the unique ```userId``` and ```movieId```
-  ```links.csv```: ??

### Merged Data: PySpark, SQL & Pandas


## New Recommender Models
### **The Pedro**
This algorithm facilitates the ability to tune recommendations to an emphasis of interest: 
* The user to movie dial
  * here we can choose how much to weight a user's own reviews versus a movie's overall reviews.
* The personality to honesty dial
  * the effect of users whose reviews don't vary much can be controlled here. The carmudgeon-factor and the I-only-give-give-reviews factor can be addressed here.  
![](images/tune-it.png)
### **We Met at the Movies**
Our models improve performance metrics, but it is difficult to make that meaningful in the context of what you really care about measuring. We are trying to measure how good you are at giving people what they want. What do people want in the context of movies? The same thing people want in the context of everything. Connection.  
Your product isn't movies. It's connection. Let's provide connection!   

> **kismet** fate, destiny, your movie soul-mates    

We have (almost) developed a way to walk through movies to each other and make new recommendations. 
This algorithm creates a group, a kismet, of people with the same movie-personality, and collection of recommended movies that the kismet hasn't seen. We would like to expand the rating interface to include space for kismets to connect by rating and discussing new movies. In addition to increasing personal connections, we are also genrating more data for better and better recommendations!
* users must opt-in to ensure that all kismet members are open to connection
* caveat that untoward behavior will buy them a ticket out of their kismet(s)

**BEST PART:** even unwanted recommendations give the kismet something to connect about...we are providing connection, remember?

## Analysis and Business Advice
found more problems and here are some more innovative solutions

<div align="center"> 
<img src="images/kayla.png" class="center">
<div align='left'> 