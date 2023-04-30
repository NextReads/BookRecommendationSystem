from math import sqrt
import numpy as np
import pandas as pd

from Utils.common_functions import *
from Utils.constants import *

# example of usage of collabortive filtering
######################################
######## data GIVEN #########
# test_user_id = "8842281e1d1347389f2ab93d60773d4d"
# test_book_read_list = ratings_df[ratings_df['user_id'] == test_user_id]['book_id'].tolist()
#
######### functions called #########
# ratings_matrix, ratings_matrix_centered = get_cf_data(test_user_id, test_book_read_list, ratings_df)
# cf_model_1 = CollaborativeFiltering(test_user_id, ratings_matrix, ratings_matrix_centered)
# predicted_books = cf_model_1.user_based_collaborative_filtering()


class CollaborativeFiltering:

    def __init__(self, user_id: str, ratings_matrix: pd.DataFrame, ratings_matrix_centered: pd.DataFrame):
        self.user_id = user_id
        self.ratings_matrix = ratings_matrix
        self.ratings_matrix_centered = ratings_matrix_centered
        self.users_pearson_similiarity = self.pearson_similiarity(
            user_id, ratings_matrix)

    def pearson_correlation(self, user1: pd.Series, user2: pd.Series) -> float:
        """
        Function to calculate the pearson correlation between two users
        :param user1: user 1
        :param user2: user 2
        :return: pearson correlation between the two users
        """
        # get the common items between the two users
        common_items = user1.index.intersection(user2.index)

        # get the ratings of the common items for each user
        user1_common_ratings = user1.loc[common_items]
        user2_common_ratings = user2.loc[common_items]

        # calculate the pearson correlation
        pearson_correlation = user1_common_ratings.corr(user2_common_ratings)

        return pearson_correlation

    def pearson_similiarity(self, user_id: str, ratings_matrix: pd.DataFrame) -> pd.DataFrame:
        """
        Function to calculate the pearson similiarity between the user and all other users
        :param user_id: user id
        :param ratings_matrix: ratings matrix
        :return: pearson similiarity between the user and all other users
        """
        # get the user row
        user_row = ratings_matrix.loc[user_id, :]

        # get the other users rows
        other_users_rows = ratings_matrix.drop(user_id)

        # calculate the pearson similiarity
        pearson_similiarity = other_users_rows.apply(
            lambda row: self.pearson_correlation(user_row, row), axis=1)

        return pearson_similiarity

    def get_top_similiar_users(self, top_users_percent: float = CF_TOP_USERS_PERCENT) -> pd.DataFrame:
        """
        Function to get the top similiar users to the user
        :param user_id: user id
        :param top_users_percent: top users percent
        :return: top similiar users to the user
        """
        # steps:
        # 1. sort the users by their pearson similiarity
        # 2. get the index of the sorted_pearson_similiarity
        # 3. get the top users percent which is the min between the index of the first nan value and the top users percent

        sorted_pearson_similiarity = self.users_pearson_similiarity.sort_values(
            ascending=False)
        first_zero_neg_index = sorted_pearson_similiarity[sorted_pearson_similiarity <= 0].index[0]

        if first_zero_neg_index == 0:
            print("No similiar users found using pearson similiarity")
            return sorted_pearson_similiarity
        else:
            first_zero_neg_location = sorted_pearson_similiarity.index.get_loc(
                first_zero_neg_index)
        top_users_percent = min(
            first_zero_neg_location, round(top_users_percent * len(sorted_pearson_similiarity)))
        top_similiar_users = sorted_pearson_similiarity.iloc[:top_users_percent]
        return top_similiar_users

    def get_not_rated_books(self) -> pd.DataFrame:
        """
        Function to find the books that the user didn't rate
        :param user_id: user id
        :return: books that the user didn't rate
        """
        # steps:
        # 1. get the user row
        # 2. get the books that the user didn't rate
        # 3. return the books that the user didn't rate

        user_row = self.ratings_matrix.loc[self.user_id, :]
        not_rated_books = user_row[user_row.isnull()].index
        return not_rated_books

    # this function follows the user-based collaborative filtering approach
    def get_predicted_rating(self) -> dict:
        """
        Function to get the predicted rating for the user
        :param user_id: user id
        :return: predicted rating for the user
        """
        # steps:
        # 1. get the top similiar users
        # 2. get the not rated books
        # 3. calculate the predicted rating by multiplying the top similiar users ratings for the not rated books with their pearson similiarity in the numerator
        # and the sum of the pearson similiarity in the denominator
        # this is done on the ratings matrix centered
        # 4. add the mean of the target user to the predicted rating
        # 5. return the predicted rating as a sorted dictionary where the key is the book id and the value is the predicted rating

        top_similiar_users = self.get_top_similiar_users()
        not_rated_books = self.get_not_rated_books()

        # explain the numerator
        # first step: we get the ratings of the top similiar users for the not rated books, this is a dataframe
        # the code responsible for first step is self.ratings_matrix_centered.loc[top_similiar_users.index, not_rated_books]
        # second step: we multiply the ratings of the top similiar users for the not rated books with their pearson similiarity
        # the code responsible for second step is self.ratings_matrix_centered.loc[top_similiar_users.index, not_rated_books].apply(lambda row: row * top_similiar_users, axis=0)
        # third step: we sum the ratings of the top similiar users for the not rated books with their pearson similiarity
        # the code responsible for third step is self.ratings_matrix_centered.loc[top_similiar_users.index, not_rated_books].apply(lambda row: row * top_similiar_users, axis=0).sum(axis=0)

        numerator = self.ratings_matrix_centered.loc[top_similiar_users.index, not_rated_books].apply(
            lambda row: row * top_similiar_users, axis=0).sum(axis=0)
        denominator = top_similiar_users.sum()
        predicted_rating = numerator / denominator

        predicted_rating = predicted_rating + \
            self.get_mean_current_user_rating()
        predicted_rating = predicted_rating.sort_values(ascending=False)
        predicted_rating_dict = predicted_rating.to_dict()
        return predicted_rating_dict

    def get_mean_current_user_rating(self):
        """
        Function to get the mean of the current user rating
        :return: mean of the current user rating
        """
        return self.ratings_matrix.loc[self.user_id, :].mean()

    def sort_prediction_around_mean(self, mean_current_user_rating: float, predicted_rating_dict: dict) -> dict:
        """
        Function to sort the predicted rating around the mean of the current user rating
        :param predicted_rating_dict: predicted rating dictionary
        :return: sorted predicted rating dictionary
        """
        # steps:
        # 1. get the mean of the current user rating
        # 2. sort the predicted rating around the mean
        # 3. return the sorted predicted rating dictionary

        sorted_predicted_rating_dict = {
            k: v for k, v in sorted(predicted_rating_dict.items(), key=lambda item: abs(item[1] - mean_current_user_rating))}
        return sorted_predicted_rating_dict

    def user_based_collaborative_filtering(self) -> dict:
        """
        Function to apply the user based collaborative filtering approach
        :return: predicted rating dictionary
        """
        # steps:
        # 1. get the predicted rating
        # 2. sort the predicted rating around the mean of the current user rating
        # 3. return the sorted predicted rating dictionary

        predicted_rating_dict = self.get_predicted_rating()
        mean_current_user_rating = self.get_mean_current_user_rating()
        sorted_predicted_rating_dict = self.sort_prediction_around_mean(
            mean_current_user_rating, predicted_rating_dict)
        return sorted_predicted_rating_dict
