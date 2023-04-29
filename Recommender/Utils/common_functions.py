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


def list_to_dataframe(my_list: list, column: list) -> pd.DataFrame:
    return pd.DataFrame(my_list, columns=column)


def check_cf_compatibilty(current_user: str, current_read_books_df: pd.DataFrame, ratings_df: pd.DataFrame) -> bool:
    # 1- check if the data is empty or the current user is not in the dataset
    if ratings_df.empty or current_read_books_df.empty or current_user not in ratings_df['user_id'].values:
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


def data_shrinking(current_user: str, current_read_books_df: pd.DataFrame, ratings_df: pd.DataFrame) -> pd.DataFrame:
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
    users_books_df = ratings_df[ratings_df['book_id'].isin(
        current_read_books_df['book_id'])]
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

    # if number_of_books == 0:
    #     return current_read_books_df

    # find all other books that have been rated by any user in users_books_df and not in current_read_books_df
    other_books_df = ratings_df[~ratings_df['book_id'].isin(
        current_read_books_df['book_id']) & ratings_df['user_id'].isin(users_books_df['user_id'])]

    # get the top CF_MAX_BOOK_NUMBER - len(current_read_books_df) books that have been rated by any user in users_books_df and not in current_read_books_df
    number_of_books = min(CF_MAX_BOOK_NUMBER - len(current_read_books_df), len(  # this
        other_books_df['book_id'].unique()))

    unique_books = other_books_df.groupby('book_id').count().sort_values(
        by='user_id', ascending=False).head(number_of_books).index

    # # add the current_read_books_df to the unique_books
    unique_books = unique_books.append(pd.Index(current_read_books_df['book_id']))
    # print the number of unique books in unique_books

    users_books_df = ratings_df[ratings_df['book_id'].isin(
        unique_books) & ratings_df['user_id'].isin(unique_users)]

    return users_books_df
