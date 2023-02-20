import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def matrix_creation():
    df = pd.read_csv('DataProcessing/dataset/goodreads_reviews_shrink.csv')
    print(df.shape)
    df.head()

    df.isnull().sum()
    df = df.dropna(subset=['review_text'])
    df.isnull().sum()

    df.shape
    print("number of unique books: ", len(df['book_id'].unique()))
    print("number of unique reviews: ", len(df['review_id'].unique()))

    def plotHIST(df, col, xlab, ylab, title):
        sns.set_style("whitegrid")
        plt.figure(figsize=(8, 6))
        plt.rc("font", size=15)
        df[col].value_counts(sort=True).plot(kind="bar")
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        plt.show()

    plotHIST(df, "rating", "Rating", "Count", "Rating Distribution")
    # remove rows with rating 0 (not rated)
    df = df[df['rating'] != 0]
    df.shape

    plotHIST(df, "rating", "Rating", "Count", "Rating Distribution")
    df['rating'].value_counts()
    # showing books
    df['book_id'].value_counts()
    # there are books that have been rated only once
    # SHRINKING THE DATASET BY REMOVING BOOKS THAT HAVE BEEN RATED LESS THAN 100 TIMES
    counts = df['book_id'].value_counts()
    df = df[df['book_id'].isin(counts[counts >= 100].index)]
    print(df.shape)
    df['book_id'].value_counts()
    df['user_id'].value_counts()
    # there are users that have rated only once
    # SHRINKING THE DATASET BY REMOVING USERS THAT HAVE RATED LESS THAN 10 TIMES
    counts = df["user_id"].value_counts()
    df = df[df["user_id"].isin(counts[counts >= 20].index)]
    print(df.shape)
    df["user_id"].value_counts()
    print(df.shape)
    df.head()

    # number of unique users and books
    print("Number of unique users: ", df["user_id"].nunique())
    print("Number of unique books: ", df["book_id"].nunique())
    df.to_csv("data_top.csv", index=False)
    # CREATING USER-ITEM MATRIX

    user_ID_test = "004d5e96c8a318aeb006af50f8cc949c"
    book_ID_test = "1"
    rating_matrix = df.pivot_table(index=["user_id"], columns=[
                                   "book_id"], values="rating")
    print(rating_matrix.shape)
    rating_matrix.head()

    mean_centered_matrix = rating_matrix.sub(
        rating_matrix.mean(axis=1), axis=0)
    print(mean_centered_matrix.shape)
    mean_centered_matrix.head()

    return rating_matrix, mean_centered_matrix
