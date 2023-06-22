import pandas as pd
def readData():
    df = pd.read_csv('../Dataset/SAafterSampling.csv',header=0,usecols=['review_text','sentiment','book_id'])
    df.head()
    return df
def datapreprocessing(data):
    # remove rows with rating 0 (not rated)
    # remove rows with nonnumeric rating
    
    data = data[data['rating'] != 3]
    data = data[data['rating'] != 0]
    print("data.shape ",data.shape)
    # data = data[data['rating'].apply(lambda x: x.isnumeric())]
    data = data[data['rating'].apply(lambda x: str(x).isdigit())]
    data['rating'] = data['rating'].astype(int)
    print("data.shape ",data.shape)

    data['sentiment'] = data['rating'].apply(lambda x: 1 if x > 3 else 0)
    print("data.shape ",data.shape)
    # remove user_id and book_id columns
    # data = data.drop(['user_id', 'book_id','rating'], axis=1)
    data = data.drop(['rating'], axis=1)
    data = data.dropna()
    return data


# function to get the avg sentiment score of every book
# creates a new dataframe for books and their avg sentiment
def getavgSentiment(books,data):
    avgSentiment = {}
    for book in set(books):
        avg=data[data['book_id']==book]['sentiment'].mean()
        count=data[data['book_id']==book]['sentiment'].count()
        avgSentiment[book] = {'avg':avg,'count':count}
    print("book_dict ",avgSentiment)

    # create a new dataframe with columns book id as dict key and and avg sentiment as
    book_sentiment_df = pd.DataFrame.from_dict(avgSentiment, orient='index')
    return book_sentiment_df

# save dataframe to csv
def saveDataframe(df,filename):
    df.to_csv(filename, index=False)
    print("saved to ",filename)