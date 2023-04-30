from nltk.tokenize import word_tokenize
from sklearn.preprocessing import normalize

def createWordSet(reviews):
    """
    Create a set of words from the reviews
    :return: set of words
    """
    wordSet = set()
    sentences=[]
    for review in reviews:
        sentence=word_tokenize(review.lower())
        sentences.append(sentence)
        # print(sentence)
        for word in sentence:
            # if word not in wordSet:
            wordSet.add(word)
    wordIndex={word:i for i,word in enumerate(wordSet)}
    # print(wordIndex)
    return wordSet,sentences


def createSentences(reviews):
    """
    Create a list of words for each reviews
    :return: list of words for each reviews
    """
    # wordSet = set()
    sentences=[]
    for review in reviews:
        sentence=word_tokenize(review.lower())
        sentences.append(sentence)
        # print(sentence)

    # wordIndex={word:i for i,word in enumerate(wordSet)}
    # print(wordIndex)
    return sentences


def wordCount(reviews,wordSet):
    """
    Count the number of words in the reviews
    :return: dictionary of word counts
    """
    wordCountDict = {}
    for review in reviews:
        for word in set(review):
            if word not in wordCountDict:
                wordCountDict[word] = 1
            else:
                wordCountDict[word] += 1
    wordIndex={word:i for i,word in enumerate(wordSet)}
    return wordCountDict,wordIndex



def termFrequency(review,word):
    """
    Calculate the term frequency of a word in a review
    :param review: a review
    :param word: a word
    :return: term frequency of the word in the review
    """
    count=0
    for w in review:
        if w==word:
            count+=1
    return count/len(review)
import math  
def inversDocumentFrequency(wordset,sentences,wordCount):
    """
    Calculate the inverse document frequency of a word in the reviews
    :param wordset: a set of words
    :param sentences: a list of reviews
    :return: inverse document frequency of the word in the reviews
    """
    
    idf={}
    numDocuments=len(sentences)
    for word in wordset:
        try:
            count=wordCount[word]+1
        except:
            count=1
        idf[word]=math.log((numDocuments+1)/(count))+1
    return idf

import numpy as np
from scipy.sparse import csr_matrix

def fit(reviews):
    """
    Calculate the tfidf of a word in the reviews
    :param reviews: a list of reviews
    :return: tfidf of the word in the reviews
    """
    wordSet,sentences=createWordSet(reviews)
    print(wordSet)
    wordSet=list(wordSet)
    # sort wordSet
    wordSet.sort()
    wordCountDict,wordIndex=wordCount(sentences,wordSet)
    # print(set(['unifying', 'amaze', 'But', 'unity', 'to','to']))
    # tfidf=csr_matrix((len(sentences),len(wordSet)),dtype=np.float64)
    idf=inversDocumentFrequency(wordSet,sentences,wordCountDict)
    # for sentence in sentences:
    #     for word in set(sentence):
    #         tfidf[word]=termFrequency(sentence,word)*inversDocumentFrequency(wordset,sentences)[word]
    # return tfidf
    print(idf)
    # for i,sentence in enumerate(sentences):
    #     for word in sentence:
            # tfidf[i]=termFrequency(sentence,word)*idf[word]
            # tfidf[i,wordIndex[word]]=termFrequency(sentence,word)*idf[word]

    return idf,wordIndex


def transform(reviews, idf, wordIndex):
    """
    Calculate the tfidf of a word in the reviews
    :param reviews: a list of reviews
    :return: tfidf of the word in the reviews
    """
    # wordSet,sentences=createWordSet(reviews)
    # wordSet=list(wordSet)
    # # sort wordSet
    # wordSet.sort()
    # wordSet1=set(sorted(wordSet))
    sentences=createSentences(reviews)
    # calculate the length of wordset from word index
    NumWords=len(wordIndex.keys())
    # print(wordSet1)
    # wordCountDict,wordIndex=wordCount(sentences,wordSet)
    # print(set(['unifying', 'amaze', 'But', 'unity', 'to','to']))
    tfidf=csr_matrix((len(sentences),NumWords),dtype=np.float64)
    # idf=inversDocumentFrequency(wordSet,sentences,wordCountDict)
    # for sentence in sentences:
    #     for word in set(sentence):
    #         tfidf[word]=termFrequency(sentence,word)*inversDocumentFrequency(wordset,sentences)[word]
    # return tfidf
    # print(idf)
    for i,sentence in enumerate(sentences):
        for word in sentence:
            if word in wordIndex.keys():
            # tfidf[i]=termFrequency(sentence,word)*idf[word]
                tfidf[i,wordIndex[word]]=termFrequency(sentence,word)*idf[word]

    return normalize(tfidf,norm='l2',axis=1,copy=True,return_norm=False)

# reviews=["amaze like felt real interact",
#          "Topic sentences are similar to mini thesis statements. Like a thesis statement",
#          "a topic sentence has a specific main point. Whereas the thesis is the main point of the essay, the topic sentence is the main point of the paragraph.               Like the thesis statement, a topic sentence has a unifying function. But a thesis statement or topic sentence alone doesn’t guarantee unity.", 
#          "An essay is unified if all the paragraphs relate to the thesis,'whereas a paragraph is unified if all the sentences relate to the topic sentence."]
# wordSet,sentences=createWordSet(reviews)
# print(wordSet)
# print(sentences)
# wordCountDict,wordIndex=wordCount(sentences, wordSet)
# print(wordCountDict)
# print(wordIndex)
# print(termFrequency(sentences[0],"amaze"))
# # print(set(['unifying', 'amaze', 'But', 'unity', 'to','to']))
# print(inversDocumentFrequency(wordSet,sentences,wordCountDict))
# #
# corpus = [
#       'this is the first document',
#       'this document is the second document',
#       'and this is the third one',
#       'is this the first document',
#  ] 
# matrix=fit_transform(reviews)
# # print(matrix) 
# print(matrix)

# from sklearn.feature_extraction.text import TfidfVectorizer

# # %load_ext autoreload
# # %autoreload 2
# # X_train,X_test,Y_train, Y_test=fe.dataSplit(df)
# tfidf = TfidfVectorizer(min_df=0.0, max_df=1.0, ngram_range=(1,2),use_idf=True, smooth_idf=True, sublinear_tf=True)
    
# tf_x_train = tfidf.fit_transform(reviews)
# print(tfidf.) 
# # print(tf_x_train)