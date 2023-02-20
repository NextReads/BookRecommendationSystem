from flask import Flask 
from flask import request
from DataProcessing.preprocessing import *
from CollabortiveFiltering.collaborative_filtering import *

app = Flask(__name__)

rating_matrix, mean_centered_matrix = matrix_creation()


# create a request handler
@app.route("/Recommendation" , methods = ['GET'])
def recommendation():
    if request.method == 'GET':
        user_ID_test = request.get_json().get('user_ID_test')
        user_based_prediction = user_based_collaborative_filtering(rating_matrix, mean_centered_matrix, user_ID_test)
        item_based_prediction = item_based_collaborative_filtering(rating_matrix, user_ID_test)
        average_prediction = average_prediction_collaborative_filtering(item_based_prediction, user_based_prediction, user_ID_test, rating_matrix)
        return average_prediction
        