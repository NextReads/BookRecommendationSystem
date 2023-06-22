# readSAdf1.csv and remove review_text column and save to another csv
import pandas as pd
# def readData():
df = pd.read_csv('Dataset/book_sentiment.csv',header=0,usecols=['sentiment','book_id'])
print(df.head())
    # return df

# save dataframe to csv
def saveDataframe(df,filename):
    df.to_csv(filename, index=False)
    print("saved to ",filename)

# covert sentiment to int
df['sentiment'] = df['sentiment'].astype(int)
# book id as string
df['book_id'] = df['book_id'].astype(str)

# create a new dataframe with columns book id and and avg sentiment and sentiment count
book_avg_sentiment = pd.DataFrame(columns=['book_id','sent_avg','sent_count'])
# df.head(10)
countloop=0
# remove rows with empty sentiment
df = df[df['sentiment'].notnull()]
# print(df.head())
# list of unique books as string
books = df['book_id'].unique()
# convert books list to string
books = books.astype(str)
print(df[df['book_id']==books[311]])
print("books ",len(books))
# calculate avg sentiment for each book

for i,book in enumerate(books):
    try:
      avg=df[df['book_id']==book]['sentiment'].mean()
      count=df[df['book_id']==book]['sentiment'].count()
      # ctrate a dataframe with book id and avg sentiment and sentiment count and index
      df1=pd.DataFrame({'book_id':book,'sent_avg':avg,'sent_count':count},index=[countloop])
      # df1= pd.DataFrame({'index':countloop,'book_id':book,'sent_avg':avg,'sent_count':count})
      # append the dataframe to book_avg_sentiment dataframe
      book_avg_sentiment= pd.concat([book_avg_sentiment,df1])
      # book_avg_sentiment = book_avg_sentiment.append({'book_id':book,'sent_avg':avg,'sent_count':count},ignore_index=True)
    except:
      # print book type
      print("error ",book,"loop ",i, "book type ",type(book))
      print(df.head())
      # print all the books with error
      # print("df: ",df[df['book_id']==book])
      exit()
    countloop+=1
    if countloop%10000==0:
        print(countloop)

saveDataframe(book_avg_sentiment,'Dataset/book_sentiment_avg_count.csv')