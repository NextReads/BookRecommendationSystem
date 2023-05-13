from math import sqrt
import numpy as np
import pandas as pd

from Utils.common_functions import *
from Utils.constants import *

from ContentBased.content_based import content_based_recommendation, content_based_recommendation_mulitple_books


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

    # function to divide the CF_MAX_BOOK_NUMBER between content based recommendations and books user already read
    def divide_max_book_number(self, current_read_books_number: int):
        threshold = int(CF_MAX_BOOK_NUMBER*CF_MAX_READ_TO_RECOMMEND_RATIO)
        if current_read_books_number < threshold:
            from_user_number = current_read_books_number
            from_content_number = CF_MAX_BOOK_NUMBER - current_read_books_number
        else:
            from_user_number = threshold
            from_content_number = CF_MAX_BOOK_NUMBER - threshold
        return from_user_number, from_content_number

    # the data coming from the database is in the form of a dictionary, so we need to convert it to a dataframe

    def dict_to_dataframe(self, current_user: str, current_read_books_dict: dict) -> pd.DataFrame:
        current_books = list(map(int, current_read_books_dict.keys()))
        current_ratings = list(map(int, current_read_books_dict.values()))

        actual_user_read_books_df = pd.DataFrame(
            {'book_id': current_books, 'user_id': current_user, 'rating': current_ratings})
        return actual_user_read_books_df

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
    # 		Getting Rating Matrix via
    # 			A- cf_user__content_all
    # 				1- Books (by collaborative filtering)
    # 				2- Users (users who read most of the books in step 1)
    def cf_user__content_all(self, current_user: str, current_read_books_df: pd.DataFrame, ratings_df: pd.DataFrame, genres_df: pd.DataFrame) -> pd.DataFrame:
        from_user_number, from_content_number = self.divide_max_book_number(
            (current_read_books_df.shape[0]))
        # 1-a Books (by conent based)
        current_read_books = current_read_books_df['book_id'].to_list()
        books_cb = content_based_recommendation_mulitple_books(
            current_read_books_df, genres_df, from_content_number)

        if books_cb.empty:
            return pd.DataFrame()
        from_content_number = len(books_cb)
        books_cb = books_cb.index.to_list()

        # 1-b Books (books read by the user)
        books_user = current_read_books[:from_user_number]

        # 2- Users (users who read most of the books in step 1)
        # get all other users who at least read one book from books_user
        users = ratings_df[ratings_df['book_id'].isin(
            books_user)]['user_id'].unique()
        # out of these users, get the ones who read at least one book from books_cb
        users_df = ratings_df[ratings_df['user_id'].isin(
            users) & ratings_df['book_id'].isin(books_cb)]

        users_number = min(
            len(users_df['user_id'].unique()), CF_MAX_USER_NUMBER)

        # get the users who read most of the books in books_cb
        users = users_df.groupby('user_id').count().sort_values(
            'book_id', ascending=False).head(users_number).index

        # NOTE:: to be removed?
        if current_user not in users:
            users = users.append(pd.Index([current_user]))

        # get the ratings of the users
        ratings = ratings_df[ratings_df['user_id'].isin(
            users) & ratings_df['book_id'].isin(books_cb + books_user)]

        return ratings

    # 			B- cf_user (Case books has no genres)
    # 				1- Users (users who read most of the target user books)
    # 				2- Books (books which are most rated by users in step 1)
    def cf_user(self, current_user: str, current_read_books_df: pd.DataFrame, ratings_df: pd.DataFrame) -> pd.DataFrame:
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

    # 	II- user, {books_IDs: ratings}, specific book_ID
    # 		Getting Rating Matrix via
    # 			A- cf_user__content_specific
    # 				1- The single book_ID (by collaborative filtering)
    # 				2- Users (users who read most of the books in step 1)

    # def cf_user__content_specific(self, current_user: str, current_read_books_df: pd.DataFrame, ratings_df: pd.DataFrame, genres_df: pd.DataFrame, book_id: str) -> pd.DataFrame:
    #     # check if the given book_id has all nan values in the genres_df
    #     if genres_df[genres_df['book_id'] == int(book_id)].isnull().all().all():
    #         return pd.DataFrame()
    #     # this has a similar structure to cf_user__content_all but using content_based_recommendation instead
    #     from_user_number, from_content_number = self.divide_max_book_number(
    #         len(current_read_books_df))
    #     # get the books from the content_based_recommendation
    #     books_cb = content_based_recommendation(
    #         book_id, genres_df, from_content_number)

    #     from_content_number = len(books_cb)

    # # 			B- Case book_ID no genre (follow steps from 2-I)

    def get_cf_rating_matrix(self, current_user: str, current_read_books_dict: dict, ratings_df: pd.DataFrame, genres_df: pd.DataFrame) -> pd.DataFrame:

        actual_user_read_books_df = self.dict_to_dataframe(
            current_user, current_read_books_dict)

        # current_read_books_df is the actual_user_read_books_df with id and rating columns dropped
        current_read_books_df = actual_user_read_books_df.drop(
            ['user_id', 'rating'], axis=1)
        current_read_books_rating_df = actual_user_read_books_df.drop(
            ['user_id'], axis=1)

        # add the df to the ratings_df
        ratings_df = pd.concat(
            [actual_user_read_books_df, ratings_df], ignore_index=True)

        # check if the data is compatible with the CF algorithm
        if not self.check_cf_compatibilty(current_user, current_read_books_df, ratings_df):
            print("The data is not compatible with the CF algorithm")
            # TODO:: calling the content_based_recommendation
            return pd.DataFrame()

        users_books_df = self.cf_user__content_all(
            current_user, current_read_books_rating_df, ratings_df, genres_df)
        if users_books_df.empty:
            print("cf_user called: case: user + books (have no equivalent genre)")
            users_books_df = self.cf_user(
                current_user, current_read_books_df, ratings_df)
        else:
            print(
                "cf_user__content_all called: case: user + books (have equivalent genre)")

        ratings_matrix = create_ratings_matrix(users_books_df)
        ratings_matrix_centered = mean_centered_rating_matrix(ratings_matrix)
        return ratings_matrix, ratings_matrix_centered
