# start by pulling the python image
FROM python:3.9.1-slim-buster

# copy every content from the local file to the image
COPY ./Recommender/ /app

# switch working directory
WORKDIR /app

RUN ls /

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME NextReadsRecommender
ENV PYTHONPATH "${PYTHONPATH}:/app/RecommenderGatewayApp"


# check if Dataset/GoodReadsShrink/goodreads_reviews_shrink.csv exists if not download it from google drive link https://drive.google.com/file/d/1ue1gnrPCmqDWTFAXyNPeP0PEoEettH0L/view
# and extract it to Dataset/GoodReadsShrink/goodreads_reviews_shrink.csv
RUN if [ ! -f "Dataset/GoodReadsShrink/goodreads_reviews_shrink.csv" ]; then \
    wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ue1gnrPCmqDWTFAXyNPeP0PEoEettH0L' -O Dataset/GoodReadsShrink/goodreads_reviews_shrink.csv; \
    fi

# Run app.py when the container launches
CMD ["RecommenderGatewayApp/app.py"]