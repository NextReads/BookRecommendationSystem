import pandas as pd
from Utils.constants import *
# %matplotlib inline
# %load_ext autoreload
# %autoreload 2
# %reload_ext autoreload


# @desc: read the goodreads books dataset from the csv file
# @param: path: the path of the csv file
# @return: the dataset as a pandas dataframe
# @type: GENERIC
def read_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


# @desc: convert the dictionary to a list of sets
# @param: my_dict: the dictionary to be converted
# @return: the list of sets
# @type: GENERIC
def dict_to_sets_list(my_dict: dict) -> list:
    # convert the dictionary to a list of sets
    my_list = []
    for item in my_dict:
        my_list.append({item, my_dict[item]})
    return my_list


# @desc: create the ratings matrix based on the dataset and the given index, columns and values
# @param: ratings_df: the dataset to be used
# @param: index: the index of the ratings matrix
# @param: columns: the columns of the ratings matrix
# @param: values: the values of the ratings matrix
# @return: the ratings matrix
# @type: GENERIC
def create_ratings_matrix(ratings_df: pd.DataFrame, index="user_id", columns="book_id", values="rating") -> pd.DataFrame:
    # create the ratings matrix
    ratings_matrix = ratings_df.pivot_table(
        index=[index], columns=[columns], values=values)
    return ratings_matrix


# @desc: gets the mean centered rating matrix
# @param: ratings_matrix: the ratings matrix to be mean centered
# @return: the mean centered rating matrix
# @type: GENERIC
def mean_centered_rating_matrix(ratings_matrix: pd.DataFrame) -> pd.DataFrame:
    # mean centering
    ratings_matrix_mean = ratings_matrix.mean(axis=1)
    ratings_matrix_centered = ratings_matrix.sub(ratings_matrix_mean, axis=0)
    return ratings_matrix_centered


def mean_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    return matrix.div(matrix.sum(axis=1), axis=0)

# @desc: decrease the size of the dataset by removing books that have been rated less than 100 times and users that have rated less than 10 times
# @param: ratings_df: the dataset to be shrunk
# @return: the shrunk dataset
# @type: SPECIFIC


def check_cf_compatibilty(current_user: str, current_read_books: list, ratings_df: pd.DataFrame) -> bool:
    # 1- check if the data is empty or the current user is not in the dataset
    if len(current_read_books) == 0 or current_user not in ratings_df['user_id'].values:
        print("the data is empty or the current user is not in the dataset")
        return False
    # 2- check if there's at least one of the current_read_books in the dataset
    if len(ratings_df[ratings_df['book_id'].isin(current_read_books)]) != 0:
        print("None of the books are in the dataset")
        return False
    # 3- check if another user has rated at least one of the current_read_books and is not the current_user
    if len(ratings_df[ratings_df['book_id'].isin(current_read_books) & (ratings_df['user_id'] != current_user)]) == 0:
        print("None of the books are rated by another user")
        return False
    return True


def data_shrinking(current_user: str, current_read_books: list, ratings_df: pd.DataFrame) -> pd.DataFrame:
    # check if the current_read_books list length is longer than the acceptable CF_MAX_BOOK_NUMBER
    if len(current_read_books) > CF_MAX_BOOK_NUMBER:
        # find the most rated CF_MAX_BOOK_NUMBER books
        current_read_books = current_read_books[:int(
            CF_MAX_BOOK_NUMBER*CF_MAX_READ_TO_RECOMMEND_RATIO)]

    # find top CF_MAX_USER_NUMBER users that have rated the most books out of the current_user's read books
    # first step: find the users that have rated any of the current_user's read books
    # second step: find the users that have rated the highest number of books out of the current_user's read books
    common_users = ratings_df[ratings_df['book_id'].isin(
        current_read_books)]['user_id']
    print("first 10 users that have rated any of the current_user's read books:" + "\n")
    print(common_users[:10])
    print(common_users.values.min())
    print(common_users.values.max())
    common_users = common_users.value_counts().index.tolist()
    print("first 10 users that have rated the highest number of books out of the current_user's read books:" + "\n")
    print(common_users[:10])
    print(common_users.values.min())
    print(common_users.values.max())
    common_users = common_users[:CF_MAX_USER_NUMBER]
    return common_users
