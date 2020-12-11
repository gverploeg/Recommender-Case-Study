import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 16})
plt.rcParams['axes.facecolor'] = 'white'
import matplotlib as mpl
mpl.rcParams['grid.color'] = 'lightgrey'
#needed for all graphs
colors = ['black', 'yellowgreen', 'thistle', 'slategrey', 'm']
alphas = [1, .5, 1, 1]
s = 5

from scipy.sparse import csr_matrix

from src.ItemItemRecommender import ItemItemRecommender
from sklearn.model_selection import train_test_split


from src.item_item_prototype import get_ratings_data, load_movies

import warnings
warnings.filterwarnings('ignore')


ratings_content = pd.read_csv('data/ml-latest-small/ratings.csv')
ratings_content.head()
ratings_content.shape # 100,836 reviews 4

utility_matrix = ratings_content.pivot_table(values='rating', index = 'userId', columns = 'movieId')
utility_matrix.to_csv('utility.csv')
utility_matrix.shape # 610 unique users, 9724 unique movies

user_ratings = (utility_matrix>0).sum(axis=1)
movie_ratings = (utility_matrix>0).sum(axis=0)
umin, umax = user_ratings.min(), user_ratings.max() #(20, 2698)
imin, imax = movie_ratings.min(), movie_ratings.max() #(1, 329)

ylim = 0,60
xlim = 0,700
fig, axs = plt.subplots(2, 1, figsize = (20,7))
axs[0].hist(user_ratings, color = colors[1], bins = umax)
axs[0].set_title('distribution: #ratings/user')
axs[0].set_xlabel('number of ratings')
# axs[0].set_ylabel('number of times we see x number of ratings')
# axs[0].set_xlim(xlim)
# axs[0].set_ylim(ylim)
axs[1].hist(movie_ratings, color = colors[4], bins = imax)
axs[1].set_title('distribution: #ratings/movie')
axs[1].set_xlabel('number of ratings')
# axs[1].set_ylabel('number of times we see x number of ratings')
# axs[1].set_xlim(xlim)
# axs[1].set_ylim(ylim)
fig.tight_layout()
fig.savefig('ratings distribution.png')
# plt.show()

utility_matrix = ratings_content.pivot_table(values='rating', index = 'userId', columns = 'movieId')
utility_matrix
utility_matrix.to_csv('utility.csv')

def sparse(df, values, rows, cols):
    piv = df.pivot_table(values = values, index = rows, columns = cols)
    tot = df.shape[0]
    user_tot = len((piv>0).sum(axis=1))
    item_tot = len((piv>0).sum(axis=0))
    return f'The density is: {tot/(user_tot*item_tot)}'
print(sparse(ratings_content, 'rating', 'userId', 'movieId'))

def sparse_loss(df, values, rows, cols, frac = 1-1/np.e, random_state=1111):
    df0 = df.sample(frac = frac, replace = False, random_state = random_state)
    piv = df0.pivot_table(values = values, index = rows, columns = cols)
    tot = df0.shape[0]
    user_tot = len((piv>0).sum(axis=1))
    item_tot = len((piv>0).sum(axis=0))
    lost_u = len(df[rows].unique()) - len(df0[rows].unique())
    lost_m = len(df[cols].unique()) - len(df0[cols].unique())
    if lost_u > 0 or lost_m >0:
        flag = 'DO'
    else:
        flag = 'DO NOT'
    return f'The split density is: {tot/(user_tot*item_tot)}\nIn our split we lost {lost_u} users and {lost_m} items\nWe {flag} have a density problem'

print(sparse_loss(ratings_content, 'rating', 'userId', 'movieId'))

average_rating = ratings_content.groupby('movieId').mean()['rating']
movies = pd.read_csv('data/ml-latest-small/movies.csv', index_col = False)
movies.set_index('movieId', inplace = True)

print(movies.loc[average_rating.idxmax()])









