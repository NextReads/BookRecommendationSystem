from math import sqrt
import numpy as np
import pandas as pd

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

    def __init__(self, rating_matrix: pd.DataFrame, mean_centered_matrix: pd.DataFrame):
        self.rating_matrix = rating_matrix
        self.mean_centered_matrix = mean_centered_matrix
        user_pearson_similarity_matrix = rating_matrix.copy()
        # use corr function to calculate pearson correlation between users (columns)
        user_pearson_similarity_matrix = user_pearson_similarity_matrix.apply(
            lambda row: row.fillna(row.mean()), axis=1)
        user_pearson_similarity_matrix = user_pearson_similarity_matrix.T.corr(
            method="pearson")
        self.user_pearson_similarity_matrix = user_pearson_similarity_matrix
        item_pearson_similarity_matrix = rating_matrix.copy()
        # use corr function to calculate pearson correlation between items (rows)
        item_pearson_similarity_matrix = item_pearson_similarity_matrix.apply(
            lambda row: row.fillna(row.mean()), axis=1)
        item_pearson_similarity_matrix = item_pearson_similarity_matrix.corr(method="pearson")
        self.item_pearson_similarity_matrix = item_pearson_similarity_matrix

    def setUserID(self, userID: str):
        self.userID = userID
    
    # FIXME: check if userId is defined
    def similar_users(self, top_users_percent: float = 0.3, threshold: float = 0.2) -> list:
        # User-based collaborative filtering
        # find the most similar users to the user
        index = self.rating_matrix.index.get_loc(self.userID)
        row_rating = self.user_pearson_similarity_matrix.iloc[index]
        row_rating.sort_values(ascending=False, inplace=True)
        top_users = round(len(self.user_pearson_similarity_matrix) * top_users_percent)
        user_list = list(row_rating.index[1:top_users+1])
        # remove users with similarity less than threshold
        user_list = [user for user in user_list if row_rating[user] > threshold]
        return user_list
    
    def find_not_rated_books(self) -> list:
        # find the books that the user has not rated
        not_rated_books = []
        not_rated_books = self.rating_matrix.loc[self.userID][self.rating_matrix.loc[self.userID].isnull()].index
        return list(not_rated_books)
    
    def predict_rating_user(self) -> dict:
        not_rated_books = self.find_not_rated_books()
        # dictionary to store the predicted rating for each book
        prediction_dict = {}
        top_users_percent = 0.3
        threshold = 0.2
        for book in not_rated_books:
            similar_users = self.similar_users(top_users_percent, threshold)
            # print("similar users for book {} are:".format(book))
            # print(similar_users)
            numerator = 0
            denominator = 0
            for user in similar_users:
                if not np.isnan(self.rating_matrix.loc[user][book]):
                    numerator += self.user_pearson_similarity_matrix.loc[self.userID][user] * \
                        self.rating_matrix.loc[user][book]
                    denominator += self.user_pearson_similarity_matrix.loc[self.userID][user]
                    # print("denominator: {}".format(denominator))
            if denominator != 0:
                prediction_dict[book] = numerator / denominator
            # print("----------------------------------------")
        # sort the dictionary by the predicted rating in descending order
        prediction_dict = {i: v for i, v in sorted(
            prediction_dict.items(), key=lambda item: item[1], reverse=True)}
        return prediction_dict
    
    def similar_items(self, itemID: str, top_items_percent: float = 0.3, threshold: float = 0.2) -> list:
        # Item-based collaborative filtering
        # find the most similar items to the item
        index = self.rating_matrix.columns.get_loc(itemID)
        row_rating = self.item_pearson_similarity_matrix.iloc[index]
        row_rating.sort_values(ascending=False, inplace=True)
        top_items = round(len(self.rating_matrix.columns) * top_items_percent)
        item_list = list(row_rating.index[1:top_items+1])
        # remove items with similarity less than threshold
        item_list = [item for item in item_list if row_rating[item] > threshold]
        return item_list
    
    def predict_rating_item(self) -> dict:
        not_rated_books = self.find_not_rated_books()
        # dictionary to store the predicted rating for each book
        prediction_dict = {}
        top_items_percent = 0.3
        threshold = 0.2
        for book in not_rated_books:
            similar_items = self.similar_items(book, top_items_percent, threshold)
            # print("similar items for book {} are:".format(book))
            # print(similar_items)
            numerator = 0
            denominator = 0
            for item in similar_items:
                if not np.isnan(self.rating_matrix.loc[self.userID][item]):
                    numerator += self.item_pearson_similarity_matrix.loc[book][item] * \
                        self.rating_matrix.loc[self.userID][item]
                    denominator += self.item_pearson_similarity_matrix.loc[book][item]
                    # print("denominator: {}".format(denominator))
            if denominator != 0:
                prediction_dict[book] = numerator / denominator
            # print("----------------------------------------")
        # sort the dictionary by the predicted rating in descending order
        prediction_dict = {i: v for i, v in sorted(
            prediction_dict.items(), key=lambda item: item[1], reverse=True)}
        return prediction_dict
    
    def user_based_collaborative_filtering(self, top_users_percent: float = 0.3, threshold: float = 0.2) -> dict:
        top_users_percent = 0.3
        mylist = self.similar_users( top_users_percent, threshold)
        user_based_prediction = self.predict_rating_user()
        # print("recommended books for user are: (Item: Rating Prediction)")
        # print(user_based_prediction)
        self.user_based_prediction = user_based_prediction
        return user_based_prediction
    
    def item_based_collaborative_filtering(self, top_items_percent: float = 0.3, threshold: float = 0.2) -> dict:
        top_items_percent = 0.3
        item_based_prediction = self.predict_rating_item()
        # print("recommended books for user are: (Item: Rating Prediction)")
        # print(item_based_prediction)
        self.item_based_prediction = item_based_prediction
        return item_based_prediction
    
    def rmse(self, prediction_dict: dict, user_mean: float):
        rmse = 0
        for item in prediction_dict:
            rmse += (prediction_dict[item] - user_mean) ** 2
        rmse = sqrt(rmse / len(prediction_dict))
        return rmse
    
    def average_prediction_collaborative_filtering(self, top_users_percent: float = 0.3, threshold: float = 0.2) -> dict:
        user_mean = self.rating_matrix.loc[self.userID].mean()
        print("user mean: {}".format(user_mean))

        # calculating average prediction from item and user CF
        average_prediction = {}
        common_items = set(self.item_based_prediction.keys()).intersection(
            set(self.user_based_prediction.keys()))
        for item in common_items:
            average_prediction[item] = (
                self.item_based_prediction[item] + self.user_based_prediction[item]) / 2

        print(average_prediction)
        

        print("RMSE for user based CF: {}".format(
            self.rmse(self.user_based_prediction, user_mean)))
        print("RMSE for item based CF: {}".format(
            self.rmse(self.item_based_prediction, user_mean)))
        print("RMSE for average prediction: {}".format(
            self.rmse(average_prediction, user_mean)))

        return average_prediction
    
    def dict_to_sets_list(self, myDict: dict) -> list:
    # convert the dictionary to a list of sets
        myList = []
        for item in myDict:
            myList.append({item, myDict[item]})
        return myList
