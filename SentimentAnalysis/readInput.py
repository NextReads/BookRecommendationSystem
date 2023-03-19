import pandas as pd
def readData():
    df = pd.read_csv('../Dataset/GoodReadsShrink/goodreads_reviews_shrink.csv',header=0,usecols=['review_text','rating'])
    df.head()
    return df
def datapreprocessing(data):
    # remove rows with rating 0 (not rated)
    data = data[data['rating'] != 0]
    data = data[data['rating'] != 3]
    # df.shape

    # plotHIST(df, "rating","Rating", "Count", "Rating Distribution")
    # data['rating'].value_counts()
    data['sentiment'] = data['rating'].apply(lambda x: 1 if x > 3 else 0)
    data = data.drop(['rating'], axis=1)
    data = data.dropna()
    return data