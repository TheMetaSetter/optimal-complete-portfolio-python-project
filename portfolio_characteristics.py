# Built-in libraries
import pandas as pd
import numpy as np
import string
import scipy.optimize as sci_opt

# User-defined libraries
import grabbing_data

#------------------------------PRE-DEFINED FUNCTIONS------------------------------

#------------------------------MAIN OBJECT------------------------------

class portfolio:
    def __init__(self, stocks_data: pd.DataFrame, num_of_stocks: int, list_of_stocks: list, risk_free_rate_year = 0.07, risk_tolerance = 20):
        
        '''
            stocks_data: historical data (the source data which contains data of list_of_stocks)
        '''
        
        ''' 
            stocks: pd.DataFrame
            num_of_stocks: <int>
            list_of_stocks: list of <class 'stocks'>
        '''
        
        self.num_of_stocks = num_of_stocks
        self.list_of_stocks = list(list_of_stocks)
        
        # self.stocks_data: stocks portfolio data
        self.stocks_data = pd.DataFrame(grabbing_data.extract_selected_stocks(stocks_data, list_of_stocks)).reset_index()
        self.stocks_data = pd.pivot_table(self.stocks_data, index = 'Date', values = 'Close', columns = 'Ticker', fill_value = None)
        
        # CHARACTERISTICS
        # Return percentage change
        self.return_pct_change = None
    
        # Mean historical return
        self.mean_historical_return = None
        
        # Variance-Covariance matrix
        self.var_covar_matrix = None
        
        # Risk free rate
        self.rf_year = risk_free_rate_year
        self.rf_month = risk_free_rate_year / 12
        
        # OPTIMAL RISKY PORTFOLIO
        # Stocks Weights
        self.stocks_weights = None
        
        # Expected return
        self.exp_ret_opt_risk = None
        
        # Expected volatility
        self.exp_volatility_opt_risk = None
        
        # Sharpe ratio
        self.sharpe_ratio = None
        
        # Optimal risky portfolio metrics
        self.opt_risk_metrics_df = None
        
        # OPTIMAL COMPLETE PORTFOLIO
        # Weights of risky portfolio and risk-free portfolio
        self.risky_weights = None
        self.risk_free_weights = None
        """
            0: risky assets
            1: risk-free assets
        """
        self.weights = None
        
        # Optimal complete portfolio expected return
        self.exp_ret_opt_com = None
        
        # Risk tolerance index A
        self.risk_tolerance = risk_tolerance
        
        # Optimal complete portfolio volatility
        self.exp_volatility_opt_com = None
        
        # Utility index
        self.utility_index = None
        
        # Optimal complete portfolio metrics
        self.opt_com_metrics_df = None
        
        # METADATA
        # Portfolio metadata
        self.meta_data = [self.opt_risk_metrics_df, self.opt_com_metrics_df]
            
    #------------------------------ONE-TIME-USE FUNCTIONS------------------------------
    # # Function to calculate return percentage change
    # def calculate_return_pct_change(self) -> pd.DataFrame:
    #     self.return_pct_change = self.stocks_data.pct_change()
        
    #     return self.return_pct_change
    
    # CONTINUE TO FIX HERE
    def calculate_return_pct_change(self) -> pd.DataFrame:
        # Create a copy of stocks data
        return_pct_change = pd.DataFrame(self.stocks_data)

        # Process on each column of the DataFrame
        merged_data_frame = None
        for column in return_pct_change.columns:
            # Extract the column
            current_column = return_pct_change[column].copy()  # Make a copy of the column
            current_column.dropna(inplace = True)  # Drop NaN values in the column
            temp_data_frame = pd.DataFrame((current_column - current_column.shift(periods = 1)) / current_column.shift(periods = 1))

            if merged_data_frame is None:
                merged_data_frame = temp_data_frame
            else:
                merged_data_frame = pd.merge(merged_data_frame, temp_data_frame, how = 'outer', left_index = True, right_index = True)

        # Assign the merged DataFrame to self.return_pct_change
        self.return_pct_change = merged_data_frame

        return self.return_pct_change

    
    # Function to calculate mean historical return
    def calculate_mean_historical_return(self) -> pd.Series:
        self.mean_historical_return = self.return_pct_change.mean(skipna = True).round(4)
        
        return self.mean_historical_return
    
    # Function to calculate variance and covariance matrix
    def calculate_variance_covariance_matrix(self) -> pd.DataFrame:
        self.var_covar_matrix = self.return_pct_change.cov(ddof = 0, numeric_only = True) / 1.014285714286 # Where does the number 1.014... come from?
        
        return self.var_covar_matrix
    
    # ------------------------------RE-USEABLE FUNCTIONS------------------------------
    
    # Generate random weights
    def generate_random_weights(self) -> np.array:
        np.random.seed(68)
        self.stocks_weights = np.array(np.random.random(self.num_of_stocks))
        self.stocks_weights = self.stocks_weights / np.sum(self.stocks_weights)
        
        return self.stocks_weights
    
    # Show stocks weights
    def show_stocks_weights(self) -> pd.Series:
        weights = pd.Series(self.stocks_weights, index = self.list_of_stocks, name = 'Stocks Weights')
        print(weights)
        
        return weights
    
    def show_weights(self) -> pd.Series:
        weights = pd.Series(self.weights, index = ['Risky assets', 'Risk-free assets'], name = 'Weights')
        print(weights)
    
    # Constraint
    def check_sum_eql_1(self, weights: list):
        return np.sum(weights) - 1
    
    def print_decor(self, str: string):
        # Decor
        print(str)
        print("=" * 50)
        
        return
    
    # ------------------------------OPTIMAL RISKY PORTFOLIO------------------------------
    
    # Function to (re)-calculate expected return
    def calculate_exp_ret_opt_risk(self) -> float:
        self.calculate_mean_historical_return()
        self.exp_ret_opt_risk = np.sum(self.mean_historical_return * self.stocks_weights)
        
        return self.exp_ret_opt_risk
    
    # Function to (re)-calculate expected volatility
    def calculate_exp_volatility_opt_risk(self) -> float:
        self.calculate_variance_covariance_matrix()
        self.exp_volatility_opt_risk = np.sqrt(
            np.dot(
                self.stocks_weights.T,
                np.dot(
                    self.var_covar_matrix,
                    self.stocks_weights
                )
            )
        )
        
        return self.exp_volatility_opt_risk
    
    # (Re)-Calculate the Sharpe ratio with an even distribution of weights
    def calculate_sharpe_ratio(self):
        self.calculate_exp_ret_opt_risk()
        self.calculate_exp_volatility_opt_risk()
        self.sharpe_ratio = (self.exp_ret_opt_risk - self.rf_month) / self.exp_volatility_opt_risk
        
        return self.sharpe_ratio
    
    # Create an initial guess for weights array
    def init_guess_weights(self, weights: list, num_of_items: float) -> np.array:
        weights = num_of_items * [1 / num_of_items]
        
        return weights
    
    # Objective function - Function calculate Sharpe ratio
    # Fixed variables: self.mean_historical_data, self.var_covar_matrix
    
    def risk_port_objective_function(self, weights: np.array) -> float:
        self.calculate_mean_historical_return()
        self.calculate_variance_covariance_matrix()
        
        # Calculate expected return
        exp_ret_opt_risk = np.sum(self.mean_historical_return * weights)
        
        # Calculate expected volatility
        exp_volatility_opt_risk = np.sqrt(
            np.dot(
                weights,
                np.dot(
                    self.var_covar_matrix,
                    weights
                )
            )
        )
        
        # Calculate sharpe ratio
        sharpe_ratio = (exp_ret_opt_risk - self.rf_month) / exp_volatility_opt_risk
        
        return -sharpe_ratio
    
    """In the maximize_sharpe function below, we will use self.stocks_weights as a parameter of 
    'opt_port_objective_function' to perform the optimization."""
    
    def maximize_sharpe(self) -> np.array:
        # Initialize self.stocks_weights array
        self.stocks_weights = self.init_guess_weights(self.stocks_weights, self.num_of_stocks)
        
        # Set constraints for decision variables
        constraints = ({'type': 'eq', 'fun': self.check_sum_eql_1})
        
        # Set bounds for decision variables
        bounds = tuple((0.05, 1) for stocks in range(self.num_of_stocks))
        
        # Optimization
        optimize_sharpe = sci_opt.minimize(
            self.risk_port_objective_function,
            self.stocks_weights,
            method = 'SLSQP',
            bounds = bounds,
            constraints = constraints
        )
        
        # After calculate the optimization, return the array of stocks weights
        self.stocks_weights = optimize_sharpe.x
        self.calculate_sharpe_ratio()
        
        return self.sharpe_ratio
    
    def show_opt_risk_metrics(self) -> None:
        if (self.sharpe_ratio == None):
            print("You have not calculated any thing!")
        else:
            self.print_decor("Optimal Risky Portfolio Metrics")
            
            # Create a dataframe containing portfolio metrics
            self.opt_risk_metrics_df = {
                "E(rp)": self.exp_ret_opt_risk,
                "σp": self.exp_volatility_opt_risk,
                "rf": self.rf_month,
                "Sharpe ratio": self.sharpe_ratio.round(4)
            }
            self.opt_risk_metrics_df = pd.DataFrame(self.opt_risk_metrics_df, index = [0])
            
            # Print metrics
            print(self.opt_risk_metrics_df)
            
        return self.opt_risk_metrics_df
    
    # ------------------------------OPTIMAL COMPLETE PORTFOLIO------------------------------
    
    # Calculate expected return of optimal complete portfolio
    def calculate_exp_re_opt_com(self) -> float:
        # self.weights = [self.risky_weights, self.risk_free_weights]
        self.exp_ret_opt_com = self.weights[0] * self.exp_volatility_opt_risk + self.weights[1] * self.rf_month
        
        return self.exp_ret_opt_com
    
    # Calculate expected volatility of optimal complete portfolio
    def calculate_exp_volatility_opt_com(self) -> float:
        # self.weights = [self.risky_weights, self.risk_free_weights]
        self.exp_volatility_opt_com = self.weights[0] * self.exp_volatility_opt_risk
        
        return self.exp_volatility_opt_com
    
    def calculate_utility_index(self) -> float:
        self.calculate_exp_re_opt_com()
        self.calculate_exp_volatility_opt_com()
        self.utility_index = self.exp_ret_opt_com - 0.5 * self.risk_tolerance * (self.exp_volatility_opt_com ** 2)
        
        return self.utility_index
    
    # Function return the utility index (U)
    def com_port_objective_function(self, weights: np.array) -> float:
        self.maximize_sharpe()
        
        # self.weights = [self.risky_weights, self.risk_free_weights]
        # Calculate expected return of optimal complete portfolio
        exp_re_opt_com = weights[0] * self.exp_ret_opt_risk + weights[1] * self.rf_month
        
        # Calculate "opt-com" portfolio volatility
        exp_volatility_opt_com = weights[0] * self.exp_volatility_opt_risk
        
        # Calculate utility index (U)
        utility_index = exp_re_opt_com - 0.5 * self.risk_tolerance * (exp_volatility_opt_com ** 2)
        
        return -utility_index
    
    # Function to maximize utility index
    def maximize_utility(self) -> float:
        # Set initial values for decision variables
        self.weights = self.init_guess_weights(self.weights, 2)
        
        # Set constraints for decision variables
        constraints = ({'type': 'eq', 'fun': self.check_sum_eql_1})
        
        # Set bounds for decision variables
        bounds = tuple((0.05, 1) for weights in range(len(self.weights)))
        
        # Optimization
        optimize_utility = sci_opt.minimize(
            self.com_port_objective_function,
            self.weights,
            method = 'SLSQP',
            bounds = bounds,
            constraints = constraints
        )
        
        # After calculate the optimization, return the array of weights
        self.weights = optimize_utility.x
        self.calculate_utility_index()
        
        return self.utility_index
    
    def maximize_utility_manual(self) -> float:
        # Calculate risky weights
        self.risky_weights = (self.exp_ret_opt_risk - self.rf_month) / (self.risk_tolerance * (self.exp_volatility_opt_risk ** 2))
        
        # Calculate risk free rate
        self.risk_free_weights = 1 - self.risky_weights
        
        # Package those weights into a single pandas series
        self.weights = [self.risky_weights, self.risk_free_weights]
        
        # Calculate expected return of optimal complete portfolio
        self.exp_ret_opt_com = self.risky_weights * self.exp_ret_opt_risk + self.risk_free_weights * self.rf_month
        
        # Calculate expected volatility of optimal complete portfolio
        self.exp_volatility_opt_com = self.risky_weights * self.exp_volatility_opt_risk
        
        # Calculate utility index
        self.utility_index = self.exp_ret_opt_com - 0.5 * self.risk_tolerance * (self.exp_volatility_opt_com ** 2)
        
        return self.utility_index
    
    def show_opt_com_metrics(self) -> None:
        if (self.utility_index == None):
            print("You have not calculated any thing!")
        else:
            self.print_decor("Optimal Complete Portfolio Metrics")
            
            # Create a dataframe containing portfolio metrics
            self.opt_com_metrics_df = {
                "E(rc)": self.exp_ret_opt_com,
                "σc": self.exp_volatility_opt_com,
                "rf": self.rf_month,
                "U": self.utility_index.round(4)
            }
            self.opt_com_metrics_df = pd.DataFrame(self.opt_com_metrics_df, index = [0])
            
            # Print metrics
            print(self.opt_com_metrics_df)
            
        return self.opt_com_metrics_df





#------------------------------GARBAGE------------------------------
# Function to maximize sharpe ratio but using cvxpy library
    # def maximize_sharpe(self):
    #     self.calculate_mean_historical_return()
    #     self.calculate_variance_covariance_matrix()
        
    #     self.stocks_weights = cp.Variable(self.num_of_stocks)
        
    #     self.init_guess_weights()
    #     self.exp_ret_opt_risk = self.stocks_weights @ self.mean_historical_return
        
    #     self.exp_volatility_opt_risk = cp.quad_form(self.stocks_weights, self.var_covar_matrix)
        
    #     self.sharpe_ratio = (self.exp_ret_opt_risk - self.rf_month) / self.exp_volatility_opt_risk
        
    #     problem = cp.Problem(cp.Maximize(self.sharpe_ratio), [cp.sum(self.stocks_weights) == 1, cp.min(self.stocks_weights) >= 0.05, cp.max(self.stocks_weights) <= 1])
        
    #     problem.solve(solver = 'SCS')
        
    #     self.sharpe_ratio = problem.value
        
    #     return self.sharpe_ratio