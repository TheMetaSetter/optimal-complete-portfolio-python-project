# Built-in libraries
import pandas as pd

# User-defined libraries
import portfolio_characteristics

# Export optimal risky portfolio to .xlsx file
def export_portfolio_to_xlsx(portfolio: portfolio_characteristics.portfolio, path = 'OTPIMAL_COMPLETE_PORTFOLIO.xlsx'):
    # Create an Excel writer object
    writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
    
    # Write percentage change
    start_row = 2
    portfolio.return_pct_change.to_excel(writer, sheet_name = 'Portfolio', startrow = start_row)
    
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Portfolio']
    
    # ------------------------------FORMAT------------------------------
    # Create a format to use in the merged range.
    merge_format = workbook.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "fg_color": "yellow",
        }
    )
    
    # Create a format to use in the heading of the percentage change of return DataFrame
    pct_heading_format = workbook.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter"
        }
    )
    
    # ------------------------------WRITE------------------------------
    # CHARACTERTISTICS
    
    # Write heading for the first step
    # Merge the cells from A2 to J2
    worksheet.merge_range('A1:D1', 'I. Calculate characteristics of all securities', merge_format)
    
    # Write the heading for the percentage change of return DataFrame
    worksheet.merge_range('A2:D2', 'Percentage change of return', pct_heading_format)
    
    # Write mean historical return
    start_row = start_row + portfolio.return_pct_change.shape[0] + 2
    pd.DataFrame(portfolio.mean_historical_return, columns = ['Mean']).to_excel(writer, sheet_name = 'Portfolio', startrow = start_row)
    
    # Write variance-covatiance matrix
    start_row = start_row + len(portfolio.mean_historical_return) + 2
    portfolio.var_covar_matrix.to_excel(writer, sheet_name = 'Portfolio', startrow = start_row)
    
    # OPTIMAL RISKY PORTFOLIO
    
    # Write stocks weight
    start_row = start_row + portfolio.var_covar_matrix.shape[0] + 3
    pd.DataFrame(portfolio.stocks_weights, index = portfolio.list_of_stocks, columns = ['Weights']).to_excel(writer, sheet_name = 'Portfolio', startrow = start_row)
    
    # Write optimal risky portfolio metrics
    start_row = start_row + len(portfolio.stocks_weights) + 3
    portfolio.opt_risk_metrics_df.to_excel(writer, sheet_name = 'Portfolio', startrow = start_row)
    
    # Write heading for the second step
    # Merge the cells
    worksheet.merge_range(f'A{start_row}:D{start_row}', 'II. Establish the optimal risky portfolio', merge_format)
    
    # OPTIMAL COMPLETE PORTFOLIO
    
    # Write weights of risky assets and risk-free assets
    start_row = start_row + portfolio.opt_risk_metrics_df.shape[0] + 3
    pd.DataFrame(portfolio.weights, index = ['Risky assets', 'Risk-free assets'], columns = ['Weights']).to_excel(writer, sheet_name = 'Portfolio', startrow = start_row)
    
    # Write optimal complete portfolio metrics
    start_row = start_row + len(portfolio.weights) + 3
    portfolio.opt_com_metrics_df.to_excel(writer, sheet_name = 'Portfolio', startrow = start_row)
    
    # Write heading for the third step
    # Merge the cells
    worksheet.merge_range(f'A{start_row}:D{start_row}', 'III. Establish the optimal complete portfolio', merge_format)
    
    # Close writer
    writer.close()
    
    return