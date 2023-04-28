from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import SparkSession
import time

json_path = 'C:/Files/College/GP/UCSDBooks/Downloads/goodreads_reviews_dedup.json'
csv_path = '../preprocessed_original/goodreads_books.csv'

columns = ['book_id', 'user_id', 'rating']
json_data = []

spark = SparkSession.builder.appName("Read JSON").getOrCreate()

chunk_size = 100000
count = 0 
time_end = time.time()
df = spark.read.json(json_path)
for chunk in df.select(col("book_id"), col("user_id"), col("rating")).rdd.glom().collect():
    # convert the chunk to a Pandas dataframe
    chunk_df = pd.DataFrame(chunk, columns=columns)
    # append the chunk to the json_data list
    json_data.append(chunk_df)
    
    # print the progress
    count += chunk_size
    time_end = time.time()
    print("finished reading {} lines in {} seconds".format(count, time_end - time_start))
