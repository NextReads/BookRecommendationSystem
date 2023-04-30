import sys


import pickle
import os


def load_model(path: str):
    pathRoot = os.getenv('NAME')
    if pathRoot == 'NextReadsRecommender':
        rPath='/app/SentimentAnalysis/models/'+path
    else:
        rPath='../SentimentAnalysis/models/'+path
    if not os.path.exists(rPath):
        raise Exception('Model not found')
    # print("model found")
    return pickle.load(open(rPath, 'rb'))


from SentimentAnalysis.preprocessing import preprocessReview
def getReviewSentiment(text):
    clflinear = load_model('svm_linear_model.sav')
    # print("model loaded")
    tfidf_vectorizer = load_model('tfidf.pkl')
    # print("tfidf loaded")
    # discard prints from the function
    text=preprocessReview(text)
    


    tfidf_test=tfidf_vectorizer.transform([text])

    prediction=clflinear.predict(tfidf_test)
    # print("predictions",predictions)
    # print("mean",mean)
    # print("prediction",prediction)
    return prediction[0]

print(getReviewSentiment(sys.argv[1]))
sys.stdout.flush()