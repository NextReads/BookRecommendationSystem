from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
import sklearn.metrics as metrics
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from tfidfVectorizer import fit,transform

def dataSplit(df):
    #Splitting the data into train and test
    X_train,X_test,Y_train, Y_test = train_test_split(df['review_text'], df['sentiment'], test_size=0.25, random_state=30)
    print("Train: ",X_train.shape,Y_train.shape,"Test: ",(X_test.shape,Y_test.shape))
    return X_train,X_test,Y_train, Y_test
    
# save and load model
def save_model(classifier, path: str):
    rPath='models/'+path
    pickle.dump(classifier, open(rPath, 'wb'))

def load_model(path: str):
    #TODO: fix this bandaid solution
    rPath='../SentimentAnalysis/models/'+path
    print(rPath)
    if not os.path.exists(rPath):
        raise Exception('Model not found')
    return pickle.load(open(rPath, 'rb'))

def featureExtractionTFIDF(X_train,X_test):
    #Feature Extraction using TF-IDF
    print("TFIDF Vectorizer……")
    tfidf = TfidfVectorizer(min_df=0.0, max_df=1.0, ngram_range=(1,2),use_idf=True, smooth_idf=True, sublinear_tf=True)
    
    tf_x_train = tfidf.fit_transform(X_train)
    tf_x_test = tfidf.transform(X_test)
    print (tf_x_train.shape, tf_x_test.shape)
    save_model(tfidf, 'tfidf.pkl')
    return tf_x_train, tf_x_test

def save_Dict(idf,wordIndex, idfName, wordIndexName):
    rPath='models/'+idfName
    pickle.dump(idf, open(rPath, 'wb'))
    rPath='models/'+wordIndexName
    pickle.dump(wordIndex, open(rPath, 'wb'))

def load_Dict(idfName, wordIndexName):
    rPath='models/'+idfName
    idf = pickle.load(open(rPath, 'rb'))
    rPath='models/'+wordIndexName
    wordIndex = pickle.load(open(rPath, 'rb'))
    return idf, wordIndex


def featureExtractionTFIDFVectorizer(X_train,X_test):
    #Feature Extraction using TF-IDF
    print("TFIDF Vectorizer……")
    # tfidf = TfidfVectorizer(min_df=0.0, max_df=1.0, ngram_range=(1,2),use_idf=True, smooth_idf=True, sublinear_tf=True)
    idf, wordIndex = fit(X_train)
    tf_x_train = transform(X_train, idf, wordIndex)
    tf_x_test = transform(X_test, idf, wordIndex)
    print (tf_x_train.shape, tf_x_test.shape)
    save_Dict(idf,wordIndex, 'idf.pkl', 'wordIndex.pkl')
    return tf_x_train, tf_x_test

def printResultsStatistics(predictions,Y_test):
    classificationReport=classification_report(Y_test, predictions, target_names=[ '0' ,  '1' ])
    CMatrix=confusion_matrix(Y_test, predictions, labels=[ '0' ,  '1' ])

    print("Confusion matrix:")
    print("\t\tpositive\tnegative")
    print("positive\t",CMatrix[0][0],"\t\t",CMatrix[0][1])
    print("negative\t",CMatrix[1][0],"\t\t",CMatrix[1][1])
    print("TP:",CMatrix[0][0],"\tFP:",CMatrix[0][1])
    print("FN:",CMatrix[1][0],"\tTN:",CMatrix[1][1])
    
    print("Accuracy:",metrics.accuracy_score(Y_test, predictions))
    print("Classification Report:")
    print(classificationReport)


def linearSVMtrain(tf_x_train,Y_train):
    #train model
    clflinear = LinearSVC(random_state=0)
    clflinear.fit(tf_x_train, Y_train)
    save_model(clflinear,'svm_linear_model.sav')

    return clflinear
    
    #evaluation

def linearSVMtest(clflinear,tf_x_test,Y_test):
    load_model('svm_linear_model.sav')
    predictionslinear = clflinear.predict(tf_x_test)
    printResultsStatistics(predictionslinear,Y_test)
    return predictionslinear


def polySVMtrain(tf_x_train,Y_train):
    #train model
    clfpoly = SVC(kernel='poly')
    clfpoly.fit(tf_x_train, Y_train)
    save_model(clfpoly,'svm_poly_model.sav')
    return clfpoly
    
    #evaluation

def polySVMtest(clfpoly,tf_x_test,Y_test):
    load_model('svm_poly_model.sav')
    predictionspoly = clfpoly.predict(tf_x_test)
    printResultsStatistics(predictionspoly,Y_test)
    return predictionspoly
    
def rbfSVMtrain(tf_x_train,Y_train):
    #train model
    clfrbf = SVC(kernel='rbf')
    clfrbf.fit(tf_x_train, Y_train)
    save_model(clfrbf,'svm_rbf_model.sav')

    return clfrbf
    
    #evaluation

def rbfSVMtest(clfrbf,tf_x_test,Y_test):
    load_model('svm_rbf_model.sav')
    predictionsrbf = clfrbf.predict(tf_x_test)
    printResultsStatistics(predictionsrbf,Y_test)
    return predictionsrbf


