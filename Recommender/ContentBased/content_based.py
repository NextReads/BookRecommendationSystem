import pandas as pd
import numpy as np
import math

from Utils.common_functions import *
from Utils.constants import *


def content_based_recommendation(book_id: int, genre_df: pd.DataFrame, N=CB_TOP_N_BOOKS):
    genre_df_copy = genre_df.copy()
    genre_df_copy = map_index_to_key(genre_df_copy)
    genre_df_copy = remove_row_has_negative(genre_df_copy)    
    tf_idf = TF_IDF_matrix(genre_df_copy)
    similarity = cosine_similarity(book_id, tf_idf)
    book_recommendations = book_recommendation(similarity)
    return book_recommendations


def map_index_to_key(genre_mean: pd.DataFrame, key="book_id") -> pd.DataFrame:
    # this function returns a dataframe with the book_id as index
    # this is done so that we can easily access the book_id of the book we want to recommend
    # and also to easily access the book_id of the books that we recommend
    book_ids = genre_mean[key]
    genre_mean = genre_mean.drop(key, axis=1)
    genre_mean.index = book_ids
    return genre_mean


def remove_row_has_negative(genre_mean: pd.DataFrame) -> pd.DataFrame:
    # find rows that have negative values in any of the columns
    result = genre_mean[genre_mean < 0].any(axis=1)
    genre_mean = genre_mean[result == False]
    return genre_mean


def remove_row_has_one(genre_mean: pd.DataFrame) -> pd.DataFrame:
    # find if there are ones in the dataframe
    result = genre_mean[genre_mean == 1].any(axis=1)
    genre_mean = genre_mean[result == False]
    return genre_mean


def IDF_matrix(genre_mean: pd.DataFrame) -> pd.DataFrame:
    # the terms are the columns and the documents are the rows
    number_of_documents = len(genre_mean)
    # calculate the Document frequency of each term which is the count on nona
    document_term_count = genre_mean.count()
    # calculate the idf for each term
    idf = document_term_count.apply(
        lambda x: math.log(number_of_documents / x))
    return idf


def TF_IDF_matrix(genre_mean: pd.DataFrame) -> pd.DataFrame:
    tf_matrix = mean_matrix(genre_mean)
    tf_matrix = remove_row_has_one(tf_matrix)
    idf_matrix = IDF_matrix(tf_matrix)
    rf_idf__matrix = tf_matrix.mul(idf_matrix, axis=1)
    return rf_idf__matrix


def cosine_similarity(book_id: int, genre_mean: pd.DataFrame) -> pd.DataFrame:
    # fill the nan values with 0 so that the np function work
    genre_mean = genre_mean.fillna(0)

    book_row = genre_mean[genre_mean.index == book_id]
    genre_mean = genre_mean[genre_mean.index != book_id]

    # calculate the dot product by multiplying element wise the two matrices and then summing the rows
    dot_product = np.multiply(genre_mean, np.asarray(book_row)).sum(axis=1)
    norm = np.linalg.norm(genre_mean, axis=1) * np.linalg.norm(
        np.asarray(book_row), axis=1)
    cosine_similarity = dot_product / norm

    # sort the cosine similarity in descending order
    cosine_similarity = cosine_similarity.sort_values(ascending=False)

    return cosine_similarity


def book_recommendation(cosine_similarity: pd.Series, N=CB_TOP_N_GENRES):
    # get the top N similar books
    book_recommendations_len = min(N, len(cosine_similarity))
    book_recommendations = cosine_similarity.head(book_recommendations_len).tolist()
    return book_recommendations


def visualize_recommendations(book_recommendations_ids: list, book_df: pd.DataFrame):
    # get info from the books dataframe
    book_recommendations = book_df[book_df['book_id'].isin(
        book_recommendations_ids)]
    book_recommendations.head(len(book_recommendations_ids))
