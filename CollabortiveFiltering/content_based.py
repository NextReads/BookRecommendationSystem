import pandas as pd
from common_functions import *


def content_based_recommendation(book_id: int, genre_df: pd.DataFrame, N=CB_TOP_N_BOOKS):
    genre_df_copy = genre_df.copy()
    genre_df_copy = remove_row_has_negative(genre_df_copy)
    genre_df_copy = weighted_matrix(genre_df_copy)
    genre_df_copy = remove_row_has_one(genre_df_copy)
    r_genres = get_highest_N_genre(book_id, genre_df_copy)
    recommendations = book_recommendations(r_genres, genre_df_copy, N)
    return recommendations


def remove_row_has_negative(genre_mean: pd.DataFrame) -> pd.DataFrame:
    # find rows that have negative values in any of the columns
    result = genre_mean[genre_mean < 0].any(axis=1)
    genre_mean = genre_mean[result == False]
    return genre_mean


def weighted_matrix(genre_mean: pd.DataFrame) -> pd.DataFrame:
    book_id = genre_mean['book_id']
    genre_mean = genre_mean.drop('book_id', axis=1)
    genre_mean = mean_matrix(genre_mean)
    genre_mean.insert(0, 'book_id', book_id)
    return genre_mean


def remove_row_has_one(genre_mean: pd.DataFrame) -> pd.DataFrame:
    # find if there are ones in the dataframe
    result = genre_mean[genre_mean == 1].any(axis=1)
    genre_mean = genre_mean[result == False]
    return genre_mean


def get_highest_N_genre(book_id: int, genre_mean: pd.DataFrame, N=CB_TOP_N_GENRES) -> pd.Series:

    # get all the columns of the book with the given id except the book_id column
    r_genres = genre_mean[genre_mean['book_id']
                          == book_id].drop('book_id', axis=1)
    r_genres = r_genres.squeeze()
    r_genre_len = min(N, len(r_genres))
    r_genres = r_genres.sort_values(ascending=False)[:r_genre_len]
    return r_genres


def book_recommendations(r_genres: pd.Series, genre_mean: pd.DataFrame, N=CB_TOP_N_BOOKS) -> pd.DataFrame:
    # sort the dataframe based on the 3 genres selected in the previous step
    genre_mean["weighted_sum"] = genre_mean[r_genres.index.to_list()].mul(
        r_genres.values, axis=1).sum(axis=1)
    genre_mean = genre_mean.sort_values(by="weighted_sum", ascending=False)
    # get first 20 books
    book_recommendations_len = min(N, len(genre_mean))
    book_recommendations = genre_mean[:book_recommendations_len]
    return book_recommendations['book_id'].to_list()


def visualize_recommendations(book_recommendations_ids: list, book_df: pd.DataFrame):
    # get info from the books dataframe
    book_recommendations = book_df[book_df['book_id'].isin(
        book_recommendations_ids)]
    book_recommendations.head(len(book_recommendations_ids))
