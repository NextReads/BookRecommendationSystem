# This file is for testing the collaborative filtering
# Steps
# 1. Load the data
# 2. Retrieve users, select a subset of them
# for every user,
from Utils.common_functions import *
from rating_matrix import *
from collaborative_filtering import *
import time
# 3. hide a percentage of their ratings
# 4. Predict the hidden ratings
# 5. export the results to a csv file
import sys
sys.path.append("../")


# Step 1: Load the data
ratings_df = read_data('../Utils/dataset/ratings.csv')
genre_df = read_data('../Utils/dataset/genres.csv')

# Step 2: Retrieve users, select a subset of them


def select_users(ratings_df: pd.DataFrame, user_number: int):
    users = ratings_df['user_id'].unique()
    # get users who has rated more than 10 books
    users = ratings_df.groupby('user_id').count()
    users = users[users['book_id'] > 10]
    users = users.index.values
    # np.random.shuffle(users)
    return users[:user_number]

# users = select_users(ratings_df, TEST_USER_NUMBER)
# Step 3: for every user, hide a percentage of their ratings, function to hide a single user's ratings, called multiple times


def hide_ratings(ratings_df: pd.DataFrame, user_id: str, ratio: float) -> pd.DataFrame:
    hidden_rating = ratings_df[ratings_df['user_id'] == user_id]
    # hide ratings of the first ratio * len(hidden_rating) books
    hidden_rating = hidden_rating.iloc[:int(ratio * len(hidden_rating))]

    # get the user non-hidden ratings
    non_hidden_ratings = ratings_df[ratings_df['user_id'] == user_id]
    non_hidden_ratings = non_hidden_ratings[~non_hidden_ratings['book_id'].isin(
        hidden_rating['book_id'])]

    return hidden_rating, non_hidden_ratings

# # find all the books that the user has rated by users[0]
# print(ratings_df[ratings_df['user_id'] == users[0]]['book_id'].unique())
# non_hidden_ratings
# rating_0
# function to get users who read at least one of the books in the hidden ratings


def get_similar_users(ratings_df: pd.DataFrame, hidden_ratings: pd.DataFrame, user_id: str):
    # get the books that the user has read
    books = hidden_ratings['book_id'].unique()
    # get the users who have read at least one of the books
    users = ratings_df[ratings_df['book_id'].isin(books)]['user_id'].unique()
    # remove the user from the list
    users = users[users != user_id]
    users_ratings = get_ratings_of_users(ratings_df, users)
    return users_ratings

# function to get the ratings of users passed in


def get_ratings_of_users(ratings_df: pd.DataFrame, users: np.ndarray):
    return ratings_df[ratings_df['user_id'].isin(users)]


# function to change fronm two columns to a dictionary, used for the non-hidden ratings
def to_dict_func(df: pd.DataFrame, key: str, value: str):
    return df.set_index(key)[value].to_dict()

# function that given a df of ratings, would get the users, find their ratings on the hidden books, merge them with the original df


def add_hidden_ratings(ratings_df: pd.DataFrame, hidden_ratings: pd.DataFrame, current_user: str):
    # this function is called after the RatingsMatrix is created and the ratings are selected
    users = ratings_df['user_id'].unique()
    # remove the user from the list
    users = users[users != current_user]
    # get the ratings of the users for the hidden books
    hidden_books = hidden_ratings['book_id'].unique()
    # get a dataframe of the ratings of the users for the hidden books
    hidden_ratings_df = ratings_df[ratings_df['book_id'].isin(
        hidden_books) & ratings_df['user_id'].isin(users)]
    # merge the hidden ratings with the original ratings
    ratings_df = pd.concat([ratings_df, hidden_ratings_df])
    # remove any duplicates rows
    ratings_df = ratings_df.drop_duplicates()

    return ratings_df

# Step 4: Predict the hidden ratings


def predict_ratings(user_id: str, read_books_dict: dict, ratings_df: pd.DataFrame, genre_df: pd.DataFrame, hidden_ratings: pd.DataFrame) -> dict:
    rm = RatingMatrix()
    users_books_df, books_cb = rm.get_final_dataframe(
        user_id, read_books_dict, ratings_df, genre_df)
    # add the hidden ratings to the ratings_df
    ratings_df = add_hidden_ratings(users_books_df, hidden_ratings, user_id)

    ratings_matrix = create_ratings_matrix(users_books_df)
    ratings_matrix_centered = mean_centered_rating_matrix(ratings_matrix)

    cf = CollaborativeFiltering(
        user_id, ratings_matrix, ratings_matrix_centered)
    predicted_books = cf.user_based_collaborative_filtering()
    print(predicted_books)
    return predicted_books


# a main function for one user
def main_one(user_id: str, ratings_df: pd.DataFrame, genre_df: pd.DataFrame, ratio: float):
    # get the hidden ratings
    non_hidden_ratings, hidden_ratings = hide_ratings(
        ratings_df, user_id, ratio)
    read_books_dict = to_dict_func(non_hidden_ratings, 'book_id', 'rating')
    # print("hidden length: ", len(hidden_ratings))
    # print("non hidden length (read): ", len(non_hidden_ratings))
    users_ratings = get_similar_users(ratings_df, hidden_ratings, user_id)
    # check if the user has read any of the books in the hidden ratings
    predictions, sentiment = predict_ratings(
        user_id, read_books_dict, users_ratings, genre_df, hidden_ratings)
    # predictions is a dictionary of book_id: predicted_rating, change it to a dataframe with columns book_id, predicted_rating
    predicted_rating = pd.DataFrame.from_dict(
        predictions, orient='index', columns=['predicted_rating'])
    # add the book_id column
    predicted_rating['book_id'] = predicted_rating.index
    # print(predicted_rating)
    return predicted_rating, hidden_ratings


ratings_df_copy = ratings_df.copy()
genre_df_copy = genre_df.copy()
TEST_USER_NUMBER = 1000
RATIO = 0.8
userrrr = "9003d274774f4c47e62f77600b08ac1d"
# [800780, 30868, 18466898, 15706923, 11950752, 614739, 7840190, 18284532, 15463724, 160495, 15750710]
# 9577969, 18306845. 377916

predicted_rating, hidden_ratings = main_one(
    userrrr, ratings_df, genre_df, RATIO)
predicted_rating.head(2)
hidden_ratings.head(2)
# rename hidden_ratings rating column to actual_rating
hidden_ratings = hidden_ratings.rename(columns={'rating': 'actual_rating'})
# drop user_id column
hidden_ratings = hidden_ratings.drop(columns=['user_id'])
# merge with predicted_rating on book_id
hidden_ratings = hidden_ratings.merge(predicted_rating, on='book_id')
hidden_ratings.head()
# def main(ratings_df: pd.DataFrame, genre_df: pd.DataFrame):
#     # split the users into two groups
#     # test_user = select_users(ratings_df, TEST_USER_NUMBER)
#     # i = 0
#     # for user in test_user:
#     ratings_df_copy = ratings_df.copy()
#     genre_df_copy = genre_df.copy()
#     predicted_rating, actual_rating = main_one(userrrr, ratings_df_copy, genre_df_copy, RATIO)
#     i += 1
#     # both are dataframes, rename the columns to be predicted and actual, then merge them on book_id
#     predicted_rating = predicted_rating.rename(columns={'rating': 'predicted'})
#     actual_rating = actual_rating.rename(columns={'rating': 'actual'})
#     merged_df = pd.merge(predicted_rating, actual_rating, on='book_id')
#     print(merged_df)

# main(ratings_df, genre_df)
# # print number of occurences of each user
# ratings_df['user_id'].value_counts()
