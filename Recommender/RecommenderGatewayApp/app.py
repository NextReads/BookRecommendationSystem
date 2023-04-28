from flask import Flask
from flask import request, jsonify
from DataProcessing.preprocessing import *
from CollabortiveFiltering.collaborative_filtering import *
from Evaluation.evaluation import *
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Gauge, Histogram
import time
from SentimentAnalysis import featureExtraction as fe
from SentimentAnalysis import classifier
from recommender import combineScores
import pandas as pd
from ContentBased.content_based import content_based_recommendation, visualize_recommendations
import Utils.common_functions as cfcf
import os

print("os.getenv('NAME') = ", os.getenv('NAME'))
app = Flask(__name__)

if os.getenv('NAME') == 'NextReadsRecommender':
    basedir = '/app/'
else:
    basedir = '../'
fileLinks = {basedir + 'Dataset/GoodReadsShrink/goodreads_reviews_shrink.csv': ('https://drive.google.com/uc?id=1ue1gnrPCmqDWTFAXyNPeP0PEoEettH0L', True),
             basedir + 'CollabortiveFiltering/dataset/goodreads_books_shrink.csv': ('https://drive.google.com/uc?id=1cvM5KArllmpjtg0CIoyLZdW_m_VGmwD5', False),
             basedir + 'CollabortiveFiltering/dataset/goodreads_genres_shrink.csv': ('https://drive.google.com/uc?id=1LCjmQ0vEBRiZtkckV6IxCoAf3V9CLKrJ', False),
             basedir + 'RecommendationGenerator/combined_score.json': ('https://drive.google.com/uc?id=1kaHSI-CGiWycpsHFOvREo5z9qwGhWTPB', False),
             basedir + 'Utils/dataset/books.csv' : ('https://drive.google.com/uc?id=1TFBNupoC2eW0P7gyIEBNcCmYGDLoljRy',False),
             basedir + 'Utils/dataset/genre.csv' : ('https://drive.google.com/uc?id=1yJGodSjJbWuCtWIWeojQ9ciS5oNdffX-',False),}

# initialize the prometheus metrics
metrics = PrometheusMetrics(app)

NR_PRECISION = Gauge(
    'nr_precision', 'Number of times the precision was calculated', ['input'])
NR_RECALL = Gauge(
    'nr_recall', 'Number of times the recall was calculated', ['input'])
NR_F1 = Gauge('nr_f1', 'Number of times the f1 was calculated', ['input'])
NR_AVERAGE_PRECISION = Gauge(
    'nr_average_precision', 'Number of times the average precision was calculated', ['input'])
NR_MRR = Gauge('nr_mrr', 'Number of times the mrr was calculated', ['input'])

NR_HISTOGRAM = Histogram('nr_recommendations_response_time_seconds', 'Response time for recommendations endpoint', buckets=(
    0.1, 0.5, 1, 2, 5, 10, 20, 30, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600))
NR_BOOKS_RECOMMENDED = Counter(
    'nr_books_recommended', 'Number of books recommended', ['input'])

rating_matrix, mean_centered_matrix = None, None
cfModel = None
data = None
cachedCombinedScoreDf = None

# create a request handler

@metrics.counter('nr_recommendation_counter', 'Number of times the recommendation endpoint was called')
@app.route("/Recommendation", methods=['GET'])
def recommendation():

    if request.method == 'GET':
        start_time = time.time()
        user_ID_test = request.get_json().get('user_ID_test')

        # check if userid is in cachedCombinedScore
        if user_ID_test in cachedCombinedScoreDf['user_id'].values:
            # get the combined score from the cache
            combined_score = cachedCombinedScoreDf[cachedCombinedScoreDf['user_id']
                                                   == user_ID_test]['combined_score'].values[0]
            return combined_score

        cfModel.setUserID(user_ID_test)
        user_based_prediction = cfModel.user_based_collaborative_filtering()
        item_based_prediction = cfModel.item_based_collaborative_filtering()
        average_prediction = cfModel.average_prediction_collaborative_filtering()
        average_prediction_list = cfModel.dict_to_sets_list(average_prediction)
        recommended, relevant, relavant_count, recommended_count, predictions = get_evaluation_data(
            average_prediction_list)
        precision, recall, f1, average_precision, mrr = get_metrics(
            recommended, relevant, relavant_count, recommended_count, predictions)
        Sentiment_score = classifier.productsSentimentScore(
            data, average_prediction)
        combined_score = combineScores(average_prediction, Sentiment_score)

        print("precision:", precision)
        print("recall:", recall)
        print("f1:", f1)
        print("average_precision:", average_precision)
        print("mrr:", mrr)

        NR_PRECISION.labels(user_ID_test).set(precision)
        NR_RECALL.labels(user_ID_test).set(recall)
        NR_F1.labels(user_ID_test).set(f1)
        NR_AVERAGE_PRECISION.labels(user_ID_test).set(average_precision)
        NR_MRR.labels(user_ID_test).set(mrr)

        response_time = time.time() - start_time
        NR_HISTOGRAM.observe(response_time)

        for book in average_prediction:
            NR_BOOKS_RECOMMENDED.labels(book).inc()

        return combined_score

# create a request handler for book with id

@metrics.counter('nr_book_counter', 'Number of times the book endpoint was called')
@app.route("/Book/<book_id>", methods=['GET'])
def book(book_id):
    if request.method == 'GET':
        start_time = time.time()
        listIds = content_based_recommendation(int(book_id), genreData)
        response_time = time.time() - start_time
        NR_HISTOGRAM.observe(response_time)
        #visData = visualize_recommendations(listIds,booksData)
        return jsonify(dict(listIds))
    
@app.route("/Start", methods=['POST'])
def start():
    # Download the dataset
    for file, url in fileLinks.items():
        if not os.path.exists(file):
            print("file doesn't exist, download it from gdrive, file: ", file)
            if url[1]:
                output = file + '.zip'
            else:
                output = file
            gdown.download(url[0], output, quiet=False)
            if url[1]:
                # unzip the file
                print("unzipping file")
                with zipfile.ZipFile(output , 'r') as zip_ref:
                    # remove unitl the last /
                    zip_ref.extractall(file[:file.rfind('/')])
                # remove the zip file
                os.remove(output)
        else:
            print("file already exists, file: ", file)

    global rating_matrix, mean_centered_matrix, cfModel, data, cachedCombinedScoreDf, genreData, booksData
    rating_matrix, mean_centered_matrix = matrix_creation()
    cfModel = CollaborativeFiltering(rating_matrix, mean_centered_matrix)

    data = classifier.readData()
    pathRoot = os.getenv('NAME')
    if pathRoot == 'NextReadsRecommender':
        genreData = cfcf.read_data('/app/CollabortiveFiltering/'+cfcf.GENRES_DF_PATH)
        booksData = cfcf.read_data('/app/CollabortiveFiltering/'+cfcf.BOOKS_DF_PATH)
    else:
        genreData = cfcf.read_data('../Utils/dataset/genre.csv')
        booksData = cfcf.read_data('../Utils/dataset/books.csv')

    try:
        if pathRoot == 'NextReadsRecommender':
            df = pd.read_json('/app/RecommendationGenerator/combined_score.json', orient='records')
        else:
            df = pd.read_json(
                "../RecommendationGenerator/combined_score.json", orient='records')
        if df.empty:
            df = pd.DataFrame(columns=['user_id', 'combined_score', 'date'])
    except:
        df = pd.DataFrame(columns=['user_id', 'combined_score', 'date'])

    
    cachedCombinedScoreDf = df

    return "Done"



@app.route('/index')
def index():
    return 'Coming Soon!'
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port)
