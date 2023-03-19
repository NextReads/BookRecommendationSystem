# Sentiment Analysis Classifier
# import pickle
import featureExtraction as fe
# %load_ext autoreload
# %autoreload 2

import pandas as pd
def readData():
    df = pd.read_csv('../dataset/goodreads_reviews_shrink.csv',header=0,usecols=['review_text','book_id'])
    df.head()
    return df
from preprocessing import preprocessing
def getProductSentiment(data,book,clflinear,tfidf_vectorizer):
    # get book review_text
    text=data[data['book_id']==book]
    # print(text)
    text=preprocessing(text)
    # print(text)
    tfidf_test=tfidf_vectorizer.transform(text['review_text'])
    # print("tfidf",tfidf_test)
    # clflinear = fe.load_model('svm_linear_model.sav')
    predictions=clflinear.predict(tfidf_test)
    # print("predictions",predictions)
    mean=predictions.mean()
    # print("mean",mean)
    return mean 

def getProductsSentiment(data,books,clflinear,tfidf_vectorizer):
    # get specific books review_text
    text=data[data['book_id'].isin(books)]
    # text=data[data['book_id']==book]
    # print(text)
    text=preprocessing(text)
    # print(text)
    text['review_text']=text['review_text'].apply(lambda x:str(x))
    tfidf_test=tfidf_vectorizer.transform(text['review_text'])
    # print("tfidf",tfidf_test)
    # clflinear = fe.load_model('svm_linear_model.sav')
    predictions=clflinear.predict(tfidf_test)
    # print("predictions",predictions)
    # mean=predictions.mean()
    # get mean predictions for each book
    mean={}
    for book in books:
        mean[book]=predictions[text['book_id']==book].mean()
    print("mean",mean)
    return mean 
# df= readData()

# clflinear = fe.load_model('svm_linear_model.sav')
# tfidf_vectorizer = fe.load_model('tfidf.pkl')
# print(getProductSentiment(df,17378508,clflinear,tfidf_vectorizer))
# books={8664353: 2.943921978404737, 6314763: 3.443921978404737, 21996: 2.778672837842172, 17378508: 3.319115269022083, 18710190: 2.943921978404737, 15797938: 2.9439219784047372, 18293427: 3.9439219784047372, 22489107: 2.77732264321156, 24612118: 2.9439219784047372, 17347389: 3.4439219784047372, 17378527: 3.321349343769989}
def sentimentScore(data,predictons):
    clflinear = fe.load_model('svm_linear_model.sav')
    tfidf_vectorizer = fe.load_model('tfidf.pkl')
    sentimentScores={}
    for book in predictons.keys():
        print(book)
        ss=getProductSentiment(data,book,clflinear,tfidf_vectorizer)
        sentimentScores[book]=ss
    return sentimentScores
# print(sentimentScore(df,books))
# books={8664353: 2.943921978404737, 6314763: 3.443921978404737, 21996: 2.778672837842172, 17378508: 3.319115269022083, 18710190: 2.943921978404737, 15797938: 2.9439219784047372, 18293427: 3.9439219784047372, 22489107: 2.77732264321156, 24612118: 2.9439219784047372, 17347389: 3.4439219784047372, 17378527: 3.321349343769989}
def productsSentimentScore(data,predictions):
    clflinear = fe.load_model('svm_linear_model.sav')
    tfidf_vectorizer = fe.load_model('tfidf.pkl')
    sentimentScores=getProductsSentiment(data,predictions,clflinear,tfidf_vectorizer)
    return sentimentScores
# ss=sentimentScore(df,books)