import pandas as pd

# example of usage
# goodreads_books_shrink = read_books_data()
# print(get_author_other_works(6066819, goodreads_books_shrink))
# print(get_author_other_works(33394837, goodreads_books_shrink))


path = 'dataset/goodreads_books_shrink.csv'

# @desc: read the goodreads books dataset from the csv file
# @param: path: the path of the csv file, default is the path of the csv file in the dataset folder
# @return: the goodreads books dataset


def read_books_data(path=path) -> pd.DataFrame:
    return pd.read_csv(path)


# @desc: get the other works of the author of the required book
# @param: required_book_id: the book ID of the required book
# @param: goodreads_books_shrink: the shrinked goodreads books dataset
# @return: list of book ID of the other works of the author of the required book


def get_author_other_works(required_book_id: int, goodreads_books_shrink: pd.DataFrame) -> list:
    author_id, series_id = goodreads_books_shrink.loc[goodreads_books_shrink['book_id'] == required_book_id, [
        'authors', 'series']].values[0]
    books_by_author = (
        goodreads_books_shrink[goodreads_books_shrink['authors'] == author_id])
    # get highest 10 rating_count books by author except required book or min of available books
    number_of_books = 10 if len(books_by_author) > 10 else len(books_by_author)
    books_by_author = books_by_author[books_by_author['book_id'] != required_book_id].sort_values(
        by='ratings_count', ascending=False).head(number_of_books)
    # get the books ID and return it as list
    return books_by_author['book_id'].tolist()
