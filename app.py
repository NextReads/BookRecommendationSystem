from flask import Flask
from flask import request
from DataProcessing.preprocessing import *
from CollabortiveFiltering.collaborative_filtering import *
from Evaluation.evaluation import *

app = Flask(__name__)

rating_matrix, mean_centered_matrix = matrix_creation()


# create a request handler
@app.route("/Recommendation", methods=['GET'])
def recommendation():
    if request.method == 'GET':
        user_ID_test = request.get_json().get('user_ID_test')
        user_based_prediction = user_based_collaborative_filtering(
            rating_matrix, mean_centered_matrix, user_ID_test)
        item_based_prediction = item_based_collaborative_filtering(
            rating_matrix, user_ID_test)
        average_prediction = average_prediction_collaborative_filtering(
            item_based_prediction, user_based_prediction, user_ID_test, rating_matrix)
        average_prediction_list = dict_to_sets_list(average_prediction)
        recommended, relevant, relavant_count, recommended_count, predictions = get_evaluation_data(
            average_prediction_list)
        precision, recall, f1, average_precision, mrr = get_metrics(
            recommended, relevant, relavant_count, recommended_count, predictions)
        print("precision:", precision)
        print("recall:", recall)
        print("f1:", f1)
        print("average_precision:", average_precision)
        print("mrr:", mrr)

        return average_prediction
