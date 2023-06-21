# Built-in libraries
import pandas as pd
import itertools

# User-defined libraries
import portfolio_characteristics
import grabbing_data

def find_optimal_risky_portfolio(stocks_data: pd.DataFrame, num_of_stocks_per_port: int, list_of_stocks: list, date_range: tuple, risk_tolerance = 20) -> portfolio_characteristics.portfolio:
    # Beatify stocks data
    stocks_data = grabbing_data.beautify_stocks_data(stocks_data)

    # Check NaN value
    # print(stocks_data.isna().sum())

    # Extract stocks_data from '2017-05-01' to '2023-05-01'
    selected_data = grabbing_data.extract_stocks_data_by_range(stocks_data, date_range)

    # Extract stocks_data of the selected stocks
    selected_data = grabbing_data.extract_selected_stocks(selected_data, list_of_stocks)

    # Extract stocks data by ['Ticker', 'Date', 'Close'] columns
    list_of_cols = ['Ticker', 'Date', 'Close']
    selected_data = grabbing_data.extract_stocks_data_by_cols(selected_data, list_of_cols)

    # Extract rows that belong to the first day appears of the month
    """This data is in long-table form."""
    selected_data = grabbing_data.extract_monthly_first_rows(selected_data)

    # CVXPY's installed solvers:  ['CVXOPT', 'ECOS', 'ECOS_BB', 'GLPK', 'GLPK_MI', 'OSQP', 'SCIPY', 'SCS']

    # Get all the groups of 3 stocks
    list_of_groups = list(itertools.combinations(list_of_stocks, num_of_stocks_per_port))
    
    # NOTICE: This will be modified to n stocks later.
    current_portfolio = None
    optimal_risky_portfolio = None
    count = 1 #To proof that there is 120 cases
    for current_group in list_of_groups:
        # Create a new portfolio of the current group
        current_portfolio = portfolio_characteristics.portfolio(selected_data, num_of_stocks_per_port, list(current_group), 0.07, risk_tolerance)
        
        # Calculate percentage change of return
        current_portfolio.calculate_return_pct_change()

        # Calculate that portfolio performance
        current_portfolio.maximize_sharpe()

        if (optimal_risky_portfolio == None):
            optimal_risky_portfolio = current_portfolio
        elif (current_portfolio.sharpe_ratio > optimal_risky_portfolio.sharpe_ratio):
            optimal_risky_portfolio = current_portfolio
        else:
            pass

        # Increase count
        count += 1

    return optimal_risky_portfolio
