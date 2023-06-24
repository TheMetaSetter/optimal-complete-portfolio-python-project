# Built-in libraries
import pandas as pd
# import cvxpy as cp

# User-defined modules
import grabbing_data
import optimal_risky_portfolio
import excel_handling

#Import stocks_data file from data folder
stocks_data = pd.read_csv('data/CafeF.HSX.Upto23.05.2023.csv')

# Beautify stocks data
stocks_data = grabbing_data.beautify_stocks_data(stocks_data)

# List of 10 selected stocks
list_of_10_stocks = ['HPG', 'NVL', 'BMP', 'GAS', 'MWG', 'SAB', 'IMP', 'MSN', 'VCB', 'VNM']

# Num of stocks in a portfolio
num_of_stocks_per_port = 3

# Set date range
date_range = (pd.to_datetime('2017-05-01'), pd.to_datetime('2023-05-31'))

port1 = optimal_risky_portfolio.find_optimal_risky_portfolio(stocks_data, num_of_stocks_per_port, list_of_10_stocks, date_range, risk_tolerance = 18)

port1.maximize_utility_manual()

port1.show_opt_risk_metrics()

port1.show_opt_com_metrics()

path1 = 'result/OPTIMAL_COMPLETE_PORTFOLIO_1.xlsx'

excel_handling.export_portfolio_to_xlsx(port1, path1)

# # List of 30 stocks
# list_of_30_stocks = ['ACB', 'BCM', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'GVR', 'HDB', 'HPG', 'MBB', 'MSN', 'MWG', 'NVL', 'PDR', 'PLX', 'POW', 'SAB', 'SSI', 'STB', 'TCB', 'TPB', 'VCB', 'VHM', 'VIB', 'VIC', 'VJC', 'VNM', 'VPB', 'VRE']

# port2 = optimal_risky_portfolio.find_optimal_risky_portfolio(stocks_data, list_of_30_stocks, date_range, risk_tolerance = 18)

# port2.maximize_utility_manual()

# port2.show_opt_risk_metrics()

# port2.show_opt_com_metrics()

# path2 = 'result/OPTIMAL_COMPLETE_PORTFOLIO_2.xlsx'

# excel_handling.export_portfolio_to_xlsx(port2, path2)