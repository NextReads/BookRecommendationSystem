# this is a class for handeling data in the form of pandas dataframes
import pandas as pd


class DataHandler:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    #############################################################
    # general methods

    def get_df(self) -> pd.DataFrame:
        return self.df

    def null_values(self) -> pd.Series:
        return self.df.isnull().sum()

    def has_negatives(self) -> bool:
        return self.df.lt(0).any().any()

    #############################################################
    # column methods

    def column_drop(self, columns: list) -> pd.DataFrame:
        """
            drops the given column(s) from the dataframe
            :param columns: list of columns to drop
            :return: the dataframe with the given columns dropped
        """
        self.df.drop(columns, axis=1, inplace=True)
        return self.df

    # get maximum and minimum values of a column
    def column_max_min(self, column: str) -> tuple:
        """
            returns a tuple of the maximum and minimum values of the given column
            :param column: the column to get the max and min values of
            :return: tuple of the max and min values
        """
        return self.df[column].max(), self.df[column].min()

    def column_float_to_int(self, column: list) -> pd.DataFrame:
        """
            converts the given column(s) to integers
            :param column: the column(s) to convert
            :return: the dataframe with the given column(s) converted to integers
        """
        self.df[column] = self.df[column].astype(int)
        return self.df

    def column_unique_values(self, column: str) -> list:
        """
            returns a list of the unique values in the given column
            :param column: the column to get the unique values of
            :return: list of the unique values
        """
        return self.df[column].unique().tolist()

    def column_replace_values(self, column: str, replace_dict: dict) -> pd.DataFrame:
        """
            replaces values in the given column with the given values
            :param column: the column to replace values in
            :param replace_dict: the dictionary of values to replace
            :return: the dataframe with the given values replaced
        """
        self.df[column].replace(replace_dict, inplace=True)
        return self.df

    def column_occurrences(self, column: str) -> pd.Series:
        """
            returns a series of the occurrences of each value in the given column
            :param column: the column to get the occurrences of
            :return: series of the occurrences of each value
        """
        return self.df[column].value_counts()
    #############################################################
    # row methods

    def row_nan_drop(self) -> pd.DataFrame:
        """
            drops rows with all nan values
            :return: the dataframe with the rows dropped
        """
        self.df.dropna(how='all', inplace=True)
        return self.df

    #############################################################
    # complex methods
    #
