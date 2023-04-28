import pandas as pd
from CollabortiveFiltering.constants import *
# %matplotlib inline
# %load_ext autoreload
# %autoreload 2
# %reload_ext autoreload


# @desc: read the goodreads books dataset from the csv file
# @param: path: the path of the csv file
# @return: the dataset as a pandas dataframe
# @type: GENERIC
def read_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


# @desc: convert the dictionary to a list of sets
# @param: my_dict: the dictionary to be converted
# @return: the list of sets
# @type: GENERIC
def dict_to_sets_list(my_dict: dict) -> list:
    # convert the dictionary to a list of sets
    my_list = []
    for item in my_dict:
        my_list.append({item, my_dict[item]})
    return my_list


# @desc: create the ratings matrix based on the dataset and the given index, columns and values
# @param: ratings_df: the dataset to be used
# @param: index: the index of the ratings matrix
# @param: columns: the columns of the ratings matrix
# @param: values: the values of the ratings matrix
# @return: the ratings matrix
# @type: GENERIC
def create_ratings_matrix(ratings_df: pd.DataFrame, index="user_id", columns="book_id", values="rating") -> pd.DataFrame:
    # create the ratings matrix
    ratings_matrix = ratings_df.pivot_table(
        index=[index], columns=[columns], values=values)
    return ratings_matrix


# @desc: gets the mean centered rating matrix
# @param: ratings_matrix: the ratings matrix to be mean centered
# @return: the mean centered rating matrix
# @type: GENERIC
def mean_centered_rating_matrix(ratings_matrix: pd.DataFrame) -> pd.DataFrame:
    # mean centering
    ratings_matrix_mean = ratings_matrix.mean(axis=1)
    ratings_matrix_centered = ratings_matrix.sub(ratings_matrix_mean, axis=0)
    return ratings_matrix_centered


def mean_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    return matrix.div(matrix.sum(axis=1), axis=0)

# @desc: decrease the size of the dataset by removing books that have been rated less than 100 times and users that have rated less than 10 times
# @param: ratings_df: the dataset to be shrunk
# @return: the shrunk dataset
# @type: SPECIFIC


def data_shrinking(ratings_df: pd.DataFrame) -> pd.DataFrame:
    ratings_df = ratings_df.dropna(subset=['review_text'])
    # remove rows with rating 0 (not rated)
    ratings_df = ratings_df[ratings_df['rating'] != 0]
    # there are books that have been rated only once
    # SHRINKING THE DATASET BY REMOVING BOOKS THAT HAVE BEEN RATED LESS THAN 100 TIMES
    counts = ratings_df['book_id'].value_counts()
    ratings_df = ratings_df[ratings_df['book_id'].isin(
        counts[counts >= 100].index)]
    # there are users that have rated only once
    # SHRINKING THE DATASET BY REMOVING USERS THAT HAVE RATED LESS THAN 10 TIMES
    counts = ratings_df["user_id"].value_counts()
    ratings_df = ratings_df[ratings_df["user_id"].isin(
        counts[counts >= 10].index)]
    return ratings_df
