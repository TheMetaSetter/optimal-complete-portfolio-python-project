import pandas as pd

# 'stocks_data' is in pandas.DataFrame datatype.

# Function to beautify the stocks_data
def beautify_stocks_data(stocks_data):
    # Replace the two '<>' characters with '' (a.k.a delete them)
    stocks_data.columns = stocks_data.columns.str.replace('<', '').str.replace('>', '')

    # Rename the 'DTYYYYMMDD' to 'Date'
    stocks_data = stocks_data.rename(columns = {'DTYYYYMMDD': 'Date'})

    # Convert the 'Date' column to a datetime datatype
    stocks_data['Date'] = pd.to_datetime(stocks_data['Date'], format = 'ISO8601')
    
    return stocks_data

# Function to extract stocks_data by range
def extract_stocks_data_by_range(stocks_data, range):
    
    '''range: <class 'tuple'>'''
    
    selected_data = stocks_data[(stocks_data['Date'] >= range[0]) & (stocks_data['Date'] <= range[1])]
    return selected_data

# Function to extract monthly first rows
def extract_monthly_first_rows(stocks_data):
    
    """
    Given a DataFrame with a 'Date' column and rows sorted in ascending order by date, 
    returns a new DataFrame with the first row that appears for each month.

    Args:
    - stocks_data (pandas.DataFrame): DataFrame with a 'Date' column and sorted by date

    Returns:
    - monthly_first_rows (pandas.DataFrame): DataFrame with first row per month
    """

    # convert 'Date' column to datetime
    stocks_data['Date'] = pd.to_datetime(stocks_data['Date'])

    # Reverse the DataFrame
    stocks_data = stocks_data.iloc[::-1]

    # group rows by year and month, and extract the first row of each group
    monthly_first_rows = stocks_data.groupby(by = ['Ticker', stocks_data['Date'].dt.year, stocks_data['Date'].dt.month]).first().droplevel(level = [1,2]).reset_index()

    return monthly_first_rows


# Function to extract stocks_data of the selected stocks to another dataframe
def extract_selected_stocks(stocks_data, list_of_stocks):
    selected_data = stocks_data[stocks_data['Ticker'].isin(list_of_stocks)]
    return selected_data

# Function to extract from stocks_data by list of columns
def extract_stocks_data_by_cols(stocks_data, list_of_cols):
    
    '''list of cols: <class 'list'>'''
    
    selected_data = pd.DataFrame(stocks_data[list_of_cols])
    return selected_data

# Function to calculate mean closing price per month
def calculate_mean_closing_price_per_month(stocks_data):
    # Convert the 'Date' column to a datetime datatype
    stocks_data['Date'] = pd.to_datetime(stocks_data['Date'], format = 'ISO8601')

    # Group the stocks_data by ticker and resample it by month end
    monthly_data = stocks_data.groupby(by = ['Ticker', pd.Grouper(key = 'Date', freq = 'MS')])['Close'].mean().reset_index()
    
    return monthly_data