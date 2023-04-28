from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import time
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("book_json_to_csv").getOrCreate()

json_path = 'C:/Files/College/GP/UCSDBooks/Downloads/goodreads_reviews_dedup.json'
csv_path = '../preprocessed_original/goodreads_books.csv'

columns = ['book_id', 'user_id', 'rating']
json_data = []

# Define the schema of the JSON file
json_schema = StructType([
    StructField("user_id", StringType()),
    StructField("book_id", StringType()),
    StructField("rating", IntegerType())
])

# Read the JSON file as a PySpark DataFrame
df = spark.read.json(json_path, schema=json_schema)

chunk_size = 100000
count = 0 
time_end = time.time()

# Iterate over the PySpark DataFrame by chunk
for chunk in df.select(columns).rdd.map(lambda row: tuple(row)).glom():
    # calculate time for each chunk
    time_start = time_end
    # append the chunk to the json_data list
    json_data.append(chunk)
    
    # print the progress
    count += chunk_size
    time_end = time.time()
    print("finished reading {} lines in {} seconds".format(count, time_end - time_start))