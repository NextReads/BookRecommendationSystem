from math import sqrt
import numpy as np
import pandas as pd

from Utils.common_functions import *
from Utils.constants import *

# example of usage of collabortive filtering
######################################
# from common_functions import *
# read_data = read_data(RATINGS_DF_PATH)
# data_shrinking = data_shrinking(read_data)
# ratings_matrix = create_ratings_matrix(data_shrinking)
# ratings_matrix_centered = mean_centered_rating_matrix(ratings_matrix)
#
#
#
# then call any of the collaborative filtering approach


class CollaborativeFiltering:

    def __init__(self, user_id: str, ratings_matrix: pd.DataFrame):
        self.ratings_matrix = ratings_matrix
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
