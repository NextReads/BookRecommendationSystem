from math import sqrt
import numpy as np
import pandas as pd

from Utils.common_functions import *
from Utils.constants import *

#






def data_shrinking(current_user: str, current_read_books_df: pd.DataFrame, ratings_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to decrease the size of the dataset by selecting users that have rated most of the target user's read books
    , then select the highest N books that have been rated by these users
    :param current_user: the current user
    :param current_read_books_df: the current user's read books
    :param ratings_df: the ratings dataset
    :return: the shrunk dataset
    """

    # check if the current_read_books_df length is longer than the acceptable CF_MAX_BOOK_NUMBER
    if len(current_read_books_df) > CF_MAX_BOOK_NUMBER:
        current_read_books_df = current_read_books_df[:CF_MAX_BOOK_NUMBER *
                                                      CF_MAX_READ_TO_RECOMMEND_RATIO]

    ##################################### GETTING THE USERS #####################################
    # find top CF_MAX_USER_NUMBER users that have rated the most books out of the current_user's read books, these users are unique
    # first step: find a subset of rating which includes all users that have rated any of the current_user's read books
    # second step: get the top CF_MAX_USER_NUMBER users that have rated the most books out of the current_user's read books, add the current_user if not there
    # third step: get a subset of the dataframe in step 1 which includes only the users in step 2

    # getting the users that have rated any of the current_user's read books
    current_books_ratings_bool = ratings_df['book_id'].isin(
        current_read_books_df['book_id'])
    users_books_df = ratings_df[current_books_ratings_bool]
    number_of_users = min(CF_MAX_USER_NUMBER, len(
        users_books_df['user_id'].unique()))
    # getting
    unique_users = users_books_df.groupby('user_id').count(
    ).sort_values(by='book_id', ascending=False).head(number_of_users).index
    # check if the current_user is in the unique_users
    if current_user not in unique_users:
        unique_users = unique_users.append(
            pd.Index([current_user]))
    # getting the highest related CF_MAX_USER_NUMBER users
    users_books_df = users_books_df[users_books_df['user_id'].isin(
        unique_users)]

    ##################################### GETTING THE BOOKS #####################################
    # first step: find all other books that have been rated by any user in users_books_df and not in current_read_books_df
    # second step: add the current_read_books_df to the unique_books
    # third step: get a subset of the original ratings_df which includes the books and users in step 1 and 2

    # find all other books that have been rated by any user in users_books_df and not in current_read_books_df
    other_books_df = ratings_df[~current_books_ratings_bool &
                                ratings_df['user_id'].isin(users_books_df['user_id'])]

    # get the top CF_MAX_BOOK_NUMBER - len(current_read_books_df) books that have been rated by any user in users_books_df and not in current_read_books_df
    number_of_books = min(CF_MAX_BOOK_NUMBER - len(current_read_books_df), len(  # this
        other_books_df['book_id'].unique()))

    unique_books = other_books_df.groupby('book_id').count().sort_values(
        by='user_id', ascending=False).head(number_of_books).index

    # # add the current_read_books_df to the unique_books
    unique_books = unique_books.append(
        pd.Index(current_read_books_df['book_id']))
    # print the number of unique books in unique_books

    users_books_df = ratings_df[ratings_df['book_id'].isin(
        unique_books) & ratings_df['user_id'].isin(unique_users)]

    return users_books_df




def get_cf_data(current_user: str, current_read_books_dict: dict, ratings_df: pd.DataFrame) -> pd.DataFrame:
    # change the current_read_books_dict to a dataframe
    """
    Function to get the data for the CF algorithm
    :param current_user: the current user id
    :param current_read_books_dict: the current user's read books, a dictionary of book_id:rating
    :param ratings_df: the ratings dataframe
    :return: the data for the CF algorithm which are the ratings matrix and the mean matrix
    """
    # steps:
    # 1. change the current_read_books_dict to a dataframe
    # 2. add the df to the ratings_df
    # 3. check if the data is compatible with the CF algorithm
    # 4. shrink the data to be compatible with the CF algorithm
    # 5. get the ratings matrix, mean matrix
    # 6. return the data

    actual_user_read_books_df, current_read_books_df = dict_to_dataframe(
        current_user, current_read_books_dict)

    # add the df to the ratings_df
    ratings_df = pd.concat(
        [actual_user_read_books_df, ratings_df], ignore_index=True)

    # check if the data is compatible with the CF algorithm
    if not check_cf_compatibilty(current_user, current_read_books_df, ratings_df):
        print("The data is not compatible with the CF algorithm")
        return pd.DataFrame()
    # shrink the data to be compatible with the CF algorithm
    users_books_df = data_shrinking(
        current_user, current_read_books_df, ratings_df)

    # print("shape of the data after shrinking: ", users_books_df.shape)
    # get the ratings matrix, mean matrix
    ratings_matrix = create_ratings_matrix(users_books_df)
    ratings_matrix_centered = mean_centered_rating_matrix(ratings_matrix)
    # return the shrunk data
    return ratings_matrix, ratings_matrix_centered
