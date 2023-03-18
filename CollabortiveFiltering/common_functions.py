import pandas as pd
from constants import *


# @desc: read the goodreads books dataset from the csv file
# @param: path: the path of the csv file
# @return: the dataset as a pandas dataframe
def read_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


# @desc: convert the dictionary to a list of sets
# @param: my_dict: the dictionary to be converted
# @return: the list of sets
def dict_to_sets_list(my_dict: dict) -> list:
    # convert the dictionary to a list of sets
    my_list = []
    for item in my_dict:
        my_list.append({item, my_dict[item]})
    return my_list


def create_ratings_matrix(ratings_df: pd.DataFrame) -> pd.DataFrame:
    # create the ratings matrix
    ratings_matrix = ratings_df.pivot_table(
        index='user_id', columns='book_id', values='rating')
    return ratings_matrix
