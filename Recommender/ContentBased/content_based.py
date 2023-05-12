import pandas as pd
import numpy as np
import math

from Utils.common_functions import *
from Utils.constants import *


def content_based_recommendation(book_id: int, genre_df: pd.DataFrame, N=CB_TOP_N_BOOKS) -> pd.Series:
    """
    Function to get the top N books for the given book id using content based recommendation
    :params book_id: book id
    :params genre_df: the dataframe that contains the genres of all books
    :params N: number of books to recommend: default value is CB_TOP_N_BOOKS
    :return: the top N books for the given book id using content based recommendation
    """
    genre_df_copy = genre_df.copy()
    genre_df_copy = map_index_to_key(genre_df_copy)
    genre_df_copy = remove_row_has_negative(genre_df_copy)
    tf_idf = TF_IDF_matrix(genre_df_copy)
    similarity = cosine_similarity(book_id, tf_idf)
    book_recommendations = book_recommendation(similarity)
    return book_recommendations


def rating_matrix_books_via_CB(book_id: list, genre_df: pd.DataFrame, N=CB_TOP_N_BOOKS) -> pd.Series:
    """
    Function to get books for the rating matrix for the books in the book_id list using content based recommendation
    :params book_id: list of book ids
    :params genre_df: the dataframe that contains the genres of all books
    :return: the books for the rating matrix for the books in the book_id list using content based recommendation
    """
    genre_df_copy = genre_df.copy()
    genres_df_subset = create_genres_df_subset(book_id, genre_df_copy)
    if len(genres_df_subset) == 0:
        return pd.DataFrame()
    new_entry = new_genre_entry(genres_df_subset)
    if len(new_entry) == 0:
        return pd.DataFrame()
    genre_df_copy = genre_df_copy.append(new_entry, ignore_index=True)
    cb_recommendation = content_based_recommendation(
        CB_IMAGINARY_BOOK_ID, genre_df_copy, N)
    return cb_recommendation


def create_genres_df_subset(book_id: list, genre_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to create a dataframe that contains the genres of the books in the book_id list
    :params book_id: list of book ids
    :params genre_df: the dataframe that contains the genres of all books
    :return: the dataframe that contains the genres of the books in the book_id list
    """
    genres_df_subset = genre_df[genre_df['book_id'].isin(book_id)]
    if len(genres_df_subset) != 0:
        genres_df_subset = remove_row_has_negative(genres_df_subset)
    return genres_df_subset


def new_genre_entry(genres_df_subset: pd.DataFrame) -> pd.DataFrame:
    """
    Function to create a new entry for the imaginary book
    :params genres_df_subset: the dataframe that contains the genres of the books in the book_id list
    :return: the dataframe that contains the new entry for the imaginary book
    """

    row_weights = genres_df_subset.sum(axis=1) / genres_df_subset.sum().sum()
    genres_df_subset = genres_df_subset.mul(row_weights, axis=0)
    new_entry = genres_df_subset.sum(axis=0)
    new_entry = new_entry.astype(int)
    # the book_id is set to CB_IMAGINARY_BOOK_ID
    new_entry['book_id'] = CB_IMAGINARY_BOOK_ID
    return new_entry


def map_index_to_key(genre_mean: pd.DataFrame, key="book_id") -> pd.DataFrame:
    """
    Function to map the index to the key
    :params genre_mean: the dataframe that contains the mean of the genres for each book
    :params key: the key to map the index to
    :return: the dataframe that contains the mean of the genres for each book with the index mapped to the key
    """
    book_ids = genre_mean[key]
    genre_mean = genre_mean.drop(key, axis=1)
    genre_mean.index = book_ids
    return genre_mean


def remove_row_has_negative(genre_mean: pd.DataFrame) -> pd.DataFrame:
    """
    Function to remove the rows that have negative values
    :params genre_mean: the dataframe that contains the mean of the genres for each book
    :return: the dataframe that contains the mean of the genres for each book without the rows that have negative values
    """
    result = genre_mean[genre_mean < 0].any(axis=1)
    genre_mean = genre_mean[result == False]
    return genre_mean


def remove_row_has_one(genre_mean: pd.DataFrame) -> pd.DataFrame:
    """
    Function to remove the rows that have negative values
    :params genre_mean: the dataframe that contains the mean of the genres for each book
    :return: the dataframe that contains the mean of the genres for each book without the rows that have negative values
    """
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
    """
    Function to calculate the tf-idf matrix
    :params genre_mean: the dataframe that contains the mean of the genres for each book
    :return: the tf-idf matrix
    """
    tf_matrix = mean_matrix(genre_mean)
    tf_matrix = remove_row_has_one(tf_matrix)
    idf_matrix = IDF_matrix(tf_matrix)
    rf_idf__matrix = tf_matrix.mul(idf_matrix, axis=1)
    return rf_idf__matrix


def cosine_similarity(book_id: int, genre_mean: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate the cosine similarity between the book_id and the other books
    :params book_id: the id of the book
    :params genre_mean: the dataframe that contains the mean of the genres for each book
    :return: the cosine similarity between the book_id and the other books
    """
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


def book_recommendation(cosine_similarity: pd.Series, N=CB_TOP_N_BOOKS) -> pd.Series:
    # get the top N similar books
    book_recommendations_len = min(N, len(cosine_similarity))
    book_recommendations = cosine_similarity.head(book_recommendations_len)
    print(book_recommendations)
    return book_recommendations


def visualize_recommendations(book_recommendations_ids: list, book_df: pd.DataFrame):
    # get info from the books dataframe
    book_recommendations = book_df[book_df['book_id'].isin(
        book_recommendations_ids)]
    book_recommendations.head(len(book_recommendations_ids))
