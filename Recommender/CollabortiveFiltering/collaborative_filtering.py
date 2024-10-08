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
        # check if pearson similiarity all values are nan
        self.sentiment = True
        if self.users_pearson_similiarity.isnull().all():
            self.sentiment = False

    def pearson_correlation(self, user1: pd.Series, user2: pd.Series) -> float:
        """
        Function to calculate the pearson correlation between two users
        :param user1: user 1
        :param user2: user 2
        :return: pearson correlation between the two users
        """
        # get the common items between the two users
        common_items = user1.index.intersection(user2.index)
        # print(" common_items: ", common_items)

        # get the ratings of the common items for each user
        user1_common_ratings = user1.loc[common_items]
        user2_common_ratings = user2.loc[common_items]
        # print(" user1_common_ratings: ", user1_common_ratings)
        # print(" user2_common_ratings: ", user2_common_ratings)

        # calculate the pearson correlation
        pearson_correlation = user1_common_ratings.corr(user2_common_ratings)
        # print(" pearson_correlation: ", pearson_correlation)
        # print("----------------------------------------")

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
        # print(" user_row: ", user_row.T)

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
        # print(" sorted_pearson_similiarity: ", sorted_pearson_similiarity)
        sorted_pearson_similiarity1 = sorted_pearson_similiarity[sorted_pearson_similiarity <= 0]
        # if it's not empty set the first_zero_neg_index to the first index of the sorted_pearson_similiarity1
        # print(" sorted_pearson_similiarity1: ", sorted_pearson_similiarity1)
        if not sorted_pearson_similiarity1.empty:
            first_zero_neg_index = sorted_pearson_similiarity1.index[0]
        else:
            first_zero_neg_index = 0

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

        similar_users = self.get_top_similiar_users()
        not_rated_books = self.get_not_rated_books()
        prediction_dict = {}

        # for every book in not_rated_books, calculate the predicted rating and add it to the prediction_dict
        for book_id in not_rated_books:
            numerator = 0
            denominator = 0
            for user in similar_users.index:
                if not np.isnan(self.ratings_matrix_centered.loc[user, book_id]):
                    numerator += self.ratings_matrix_centered.loc[user, book_id] * \
                        similar_users[user]
                    denominator += similar_users[user]
            if denominator == 0:
                prediction_dict[book_id] = 0
            else:
                prediction_dict[book_id] = numerator / denominator

        # add the mean of the current user rating to the predicted rating
        mean_current_user_rating = self.get_mean_current_user_rating()
        prediction_dict = {
            k: v + mean_current_user_rating for k, v in prediction_dict.items()}
        return prediction_dict

    def get_mean_current_user_rating(self):
        """
        Function to get the mean of the current user rating
        :return: mean of the current user rating
        """
        return self.ratings_matrix.loc[self.user_id, :].mean()

    def sort_prediction_descedingly(self, predicted_rating_dict: dict) -> dict:
        """
        Function to sort the predicted rating dictionary descedingly
        :param predicted_rating_dict: predicted rating dictionary
        :return: sorted predicted rating dictionary
        """
        # steps:
        # 1. sort the predicted rating dictionary descedingly
        # 2. return the sorted predicted rating dictionary

        sorted_predicted_rating_dict = dict(
            sorted(predicted_rating_dict.items(), key=lambda item: item[1], reverse=True))
        return sorted_predicted_rating_dict

    def sort_prediction_according_to_mean(self, predicted_rating_dict: dict) -> dict:
        mean = self.get_mean_current_user_rating()
        sorted_predicted_rating_dict = dict(
            sorted(predicted_rating_dict.items(), key=lambda item: abs(item[1]-mean), reverse=False))
        return sorted_predicted_rating_dict
    
    def sort_prediction_according_to_max(self, predicted_rating_dict: dict) -> dict:
        max = self.ratings_matrix.loc[self.user_id, :].max()
        sorted_predicted_rating_dict = dict(
            sorted(predicted_rating_dict.items(), key=lambda item: abs(item[1]-max), reverse=False))
        return sorted_predicted_rating_dict

    def remove_books_with_low_rating(self, predicted_rating_dict: dict) -> dict:
        """
        Function to remove any book that has rating less than user's minimum rating
        :param predicted_rating_dict: predicted rating dictionary
        :return: predicted rating dictionary
        """

        minimum_rating = self.ratings_matrix.loc[self.user_id, :].min()
        predicted_rating_dict = {
            k: v for k, v in predicted_rating_dict.items() if v >= minimum_rating}
        return predicted_rating_dict

    def user_based_collaborative_filtering(self) -> dict:
        """
        Function to apply the user based collaborative filtering approach, calls the get_predicted_rating and sort_prediction_descedingly functions
        :return: predicted rating dictionary
        """
        # steps:
        # 1. get the predicted rating
        # 2. sort the predicted rating around the mean of the current user rating
        # 3. return the sorted predicted rating dictionary
        sorted_predicted_rating_dict = {}
        if self.sentiment == True:
            predicted_rating_dict = self.get_predicted_rating()
            # remove all nan values from predicted_rating_dict
            predicted_rating_dict = {
                k: v for k, v in predicted_rating_dict.items() if not np.isnan(v)}
            sorted_predicted_rating_dict = self.sort_prediction_according_to_max(
                predicted_rating_dict)
            sorted_predicted_rating_dict = self.remove_books_with_low_rating(
                sorted_predicted_rating_dict)
            # check if the sorted_predicted_rating_dict is empty
            if len(sorted_predicted_rating_dict) == 0:
                self.sentiment = False
        return sorted_predicted_rating_dict, self.sentiment
