from math import sqrt
import numpy as np
import pandas as pd


def find_not_rated_books(userID: str, rating_matrix: pd.DataFrame):
    not_rated_books = rating_matrix.loc[userID][rating_matrix.loc[userID].isnull(
    )].index
    return list(not_rated_books)


def user_based_collaborative_filtering(rating_matrix: pd.DataFrame, mean_centered_matrix: pd.DataFrame, userID: str) -> dict:

    user_ID_test = userID

    # User-based collaborative filtering
    user_pearson_similarity_matrix = rating_matrix.copy()

    # use corr function to calculate pearson correlation between users (columns)
    user_pearson_similarity_matrix = user_pearson_similarity_matrix.apply(
        lambda row: row.fillna(row.mean()), axis=1)
    user_pearson_similarity_matrix = user_pearson_similarity_matrix.T.corr(
        method="pearson")

    def similar_users(userID: str, top_percent: int, threshold: float = 0.2):
        index = rating_matrix.index.get_loc(userID)
        row_rating = user_pearson_similarity_matrix.iloc[index]
        row_rating.sort_values(ascending=False, inplace=True)
        top_users = round(len(user_pearson_similarity_matrix) * top_percent)
        user_list = list(row_rating.index[1:top_users+1])
        # remove users with similarity less than threshold
        user_list = [
            user for user in user_list if row_rating[user] > threshold]
        return user_list

    # this function predicts the rating of the missing values in the rating matrix for a given user given a list of similar users

    def predict_rating_user(userID: str, userIDs: list):
        # get the not rated books by the user
        not_rated_books = find_not_rated_books(userID, rating_matrix)
        # dictionary to store the predicted rating for each book
        prediction_dict = {}
        for book in not_rated_books:
            numerator = 0
            denominator = 0
            for user in userIDs:
                if not np.isnan(rating_matrix.loc[user][book]):
                    numerator += user_pearson_similarity_matrix.loc[userID][user] * \
                        mean_centered_matrix.loc[user][book]
                    denominator += user_pearson_similarity_matrix.loc[userID][user]
            if denominator != 0:
                prediction_dict[book] = numerator / \
                    denominator + rating_matrix.loc[userID].mean()

        # sort the dictionary by the predicted rating in descending order
        prediction_dict = {i: v for i, v in sorted(
            prediction_dict.items(), key=lambda item: item[1], reverse=True)}
        return prediction_dict

    top_users_percent = 0.3
    mylist = similar_users(userID, top_users_percent)
    user_based_prediction = predict_rating_user(
        userID, mylist)
    # print("recommended books for user are: (Item: Rating Prediction)")
    # print(user_based_prediction)
    return user_based_prediction


def item_based_collaborative_filtering(rating_matrix: pd.DataFrame, userID: str) -> dict:
    # Item-based collaborative filtering
    item_pearson_similarity_matrix = rating_matrix.copy()
    # use corr function to calculate pearson correlation between users (columns)
    item_pearson_similarity_matrix = item_pearson_similarity_matrix.apply(
        lambda row: row.fillna(row.mean()), axis=1)
    item_pearson_similarity_matrix = item_pearson_similarity_matrix.corr(
        method="pearson")

    def similar_items(itemID: str, top_items_number: int = len(rating_matrix.columns), threshold: float = 0.2):
        index = rating_matrix.columns.get_loc(itemID)
        coloumn_rating = item_pearson_similarity_matrix.iloc[index]
        coloumn_rating.sort_values(ascending=False, inplace=True)
        top_items = min(len(item_pearson_similarity_matrix), top_items_number)
        item_list = list(coloumn_rating.index[1:top_items+1])
        # remove items with similarity less than threshold
        item_list = [
            item for item in item_list if coloumn_rating[item] > threshold]
        return item_list

    def predict_rating_item(userID: str):
        not_rated_books = find_not_rated_books(userID, rating_matrix)
        # dictionary to store the predicted rating for each book
        prediction_dict = {}
        top_items_number = round(sqrt(len(rating_matrix.columns)))

        for book in not_rated_books:
            similar_books = similar_items(book, top_items_number)
            # print("similar books for book {} are:".format(book))
            # print(similar_books)
            numerator = 0
            denominator = 0
            for item in similar_books:
                if not np.isnan(rating_matrix.loc[userID][item]):
                    numerator += item_pearson_similarity_matrix.loc[book][item] * \
                        rating_matrix.loc[userID][item]
                    denominator += item_pearson_similarity_matrix.loc[book][item]
                    # print("denominator: {}".format(denominator))
            if denominator != 0:
                prediction_dict[book] = numerator / denominator
            # print("----------------------------------------")
        # sort the dictionary by the predicted rating in descending order
        prediction_dict = {i: v for i, v in sorted(
            prediction_dict.items(), key=lambda item: item[1], reverse=True)}
        return prediction_dict
    # Item-based collaborative filtering test
    # case item searched, with no clue who the user is
    # item_prediction = similar_items(968)
    # print(item_prediction)

    # case user logged in
    item_based_prediction = predict_rating_item(userID)
    # print(item_based_prediction)

    return item_based_prediction


def average_prediction_collaborative_filtering(item_based_prediction: dict, user_based_prediction: dict, user_ID_test: str, rating_matrix: pd.DataFrame) -> dict:
    # Final predictions & statistics
    user_mean = rating_matrix.loc[user_ID_test].mean()
    print("user mean: {}".format(user_mean))

    # calculating average prediction from item and user CF
    average_prediction = {}
    common_items = set(item_based_prediction.keys()).intersection(
        set(user_based_prediction.keys()))
    for item in common_items:
        average_prediction[item] = (
            item_based_prediction[item] + user_based_prediction[item]) / 2

    print(average_prediction)

    # calculating the RMSE

    def rmse(prediction_dict: dict, user_mean: float):
        rmse = 0
        for item in prediction_dict:
            rmse += (prediction_dict[item] - user_mean) ** 2
        rmse = sqrt(rmse / len(prediction_dict))
        return rmse

    print("RMSE for user based CF: {}".format(
        rmse(user_based_prediction, user_mean)))
    print("RMSE for item based CF: {}".format(
        rmse(item_based_prediction, user_mean)))
    print("RMSE for average prediction: {}".format(
        rmse(average_prediction, user_mean)))

    return average_prediction
