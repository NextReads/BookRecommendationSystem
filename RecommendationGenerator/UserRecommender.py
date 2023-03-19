import repackage
repackage.up()
from DataProcessing.preprocessing import *
from CollabortiveFiltering.collaborative_filtering import *
from Evaluation.evaluation import *
from SentimentAnalysis import featureExtraction as fe
from SentimentAnalysis import classifier
from RecommenderGatewayApp.recommender import combineScores
import datetime
import json
import pandas as pd


def fetchUsers():
    rating_matrix, mean_centered_matrix = matrix_creation()
    return rating_matrix, mean_centered_matrix

def recommendUser(rating_matrix, mean_centered_matrix):
    # print all user_id from dataframe
    cfModel = CollaborativeFiltering(rating_matrix, mean_centered_matrix)
    data = classifier.readData()
    # read json file to dataframe and check if its empty
    try:
        df = pd.read_json("./combined_score.json", orient='records')
        if df.empty:
            df = pd.DataFrame(columns=['user_id', 'combined_score', 'date'])
    except:
        df = pd.DataFrame(columns=['user_id', 'combined_score', 'date'])
    for user in rating_matrix.index:
        date = datetime.datetime.now()
        # check if user already exists in json file
        if user in df['user_id'].values:
            # check if older than month
            if (date - df.loc[df['user_id'] == user, 'date'].values[0]).days < 30:
                continue
        cfModel.setUserID(user)
        user_based_prediction = cfModel.user_based_collaborative_filtering()
        item_based_prediction = cfModel.item_based_collaborative_filtering()
        average_prediction = cfModel.average_prediction_collaborative_filtering()
        average_prediction_list = cfModel.dict_to_sets_list(average_prediction)
        recommended, relevant, relavant_count, recommended_count, predictions = get_evaluation_data(
            average_prediction_list)
        precision, recall, f1, average_precision, mrr = get_metrics(
            recommended, relevant, relavant_count, recommended_count, predictions)
        Sentiment_score = classifier.productsSentimentScore(data, average_prediction)
        combined_score = combineScores(average_prediction, Sentiment_score)

        # append to dataframe
        df = df.append({'user_id': user, 'combined_score': combined_score, 'date': date}, ignore_index=True)

        # save to json file
        df.to_json("./combined_score.json", orient='records')

        
        return




