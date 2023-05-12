from math import sqrt
import numpy as np
import pandas as pd

from Utils.common_functions import *
from Utils.constants import *


# This class is used to create the ratings matrix and the ratings matrix centered
# we have multiple cases to cover:
# 1- USER RATED BOOKS ISNOT RATED BY ANY USERS
# 	II- static recommendations


# 2- USER RATED BOOKS ARE RATED BY OTHERS
# 	I- user, {books_IDs: ratings}
# 		Getting Rating Matrix via
# 			A- cf_user__content_all
# 				1- Books (by collaborative filtering)
# 				2- Users (users who read most of the books in step 1)

# 			B- cf_user (Case books has no genres)
# 				1- Users (users who read most of the target user books)
# 				2- Books (books which are most rated by users in step 1)


# 	II- user, {books_IDs: ratings}, specific book_ID
# 		Getting Rating Matrix via
# 			A- cf_user__content_specific
# 				1- The single book_ID (by collaborative filtering)
# 				2- Users (users who read most of the books in step 1)

# 			B- Case book_ID no genre (follow steps from 2-I)


class RatingMatrix:

    # the data coming from the database is in the form of a dictionary, so we need to convert it to a dataframe
    def dict_to_dataframe(self, current_user: str, current_read_books_dict: dict) -> pd.DataFrame:
        current_books = list(map(int, current_read_books_dict.keys()))
        current_ratings = list(map(int, current_read_books_dict.values()))

        actual_user_read_books_df = pd.DataFrame(
            {'book_id': current_books, 'user_id': current_user, 'rating': current_ratings})
        current_read_books_df = list_to_dataframe(
            current_books, ['book_id'])
        return actual_user_read_books_df, current_read_books_df

    # rating matrix is used for the collaborative filtering algorithm, hence we need to check if the current user is compatible with the algorithm

    def check_cf_compatibilty(self, current_user: str, current_read_books_df: pd.DataFrame, ratings_df: pd.DataFrame) -> bool:
        """
        Function to check if the current user is compatible with the collaborative filtering algorithm
        :param current_user: the current user
        :param current_read_books_df: the current user's read books
        :param ratings_df: the ratings dataset
        :return: True if the current user is compatible with the collaborative filtering algorithm, False otherwise
        """

        # checkings include:
        # 1- check if the data is empty
        # 2- check if there's at least one of the books_id column in the current_read_books_df exists in the ratings_df
        # 3- check if another user has rated at least one of the current_read_books and is not the current_user

        # 1- check if the data is empty or the current user is not in the dataset
        if ratings_df.empty or current_read_books_df.empty:
            print("the data is empty or the current user is not in the dataset")
            return False
        # 2- check if there's at least one of the books_id column in the current_read_books_df exists in the ratings_df
        is_common_books = ratings_df['book_id'].isin(
            current_read_books_df['book_id'])
        if len(ratings_df[is_common_books]) == 0:
            print("None of the books are in the dataset")
            return False
        # 3- check if another user has rated at least one of the current_read_books and is not the current_user
        if len(ratings_df[is_common_books & (ratings_df['user_id'] != current_user)]) == 0:
            print("None of the books are rated by another user")
            return False
        return True

    ##############################################################################################################
    ##############################################################################################################
    # 1- USER RATED BOOKS ISNOT RATED BY ANY USERS

    # 2- USER RATED BOOKS ARE RATED BY OTHERS
    # 	I- user, {books_IDs: ratings}
    #         A- cf_user__content_all

    def cf_user__content_all
