
# Optimal Complete Portfolio Establisher

## Overview

The **Optimal Complete Portfolio Establisher** is a Python-based tool designed to help users establish an optimal complete portfolio by utilizing various financial models and data analysis techniques. This tool aims to assist users in finding the best portfolio mix that balances risk and return according to their financial goals.

## Features

- **Data Grabbing**: Collect financial data from [Dữ liệu lịch sử cho MetaStock và AmiBroker](https://s.cafef.vn/du-lieu-download.chn#data){:target="_blank"}.
- **Portfolio Analysis**: Analyze portfolio characteristics, such as expected return, risk, and optimal allocation.
- **Risky Portfolio Optimization**: Find the optimal risky portfolio using various financial metrics.
- **Excel Integration**: Export portfolio characteristics and results to an Excel file for further analysis.

## Files

- **main.py**: The main script that integrates all the modules and runs the complete portfolio establishment process.
- **grabbing_data.py**: Handles the extraction and processing of financial data required for portfolio analysis.
- **optimal_risky_portfolio.py**: Contains functions and algorithms to calculate the optimal risky portfolio.
- **portfolio_characteristics.py**: Computes the characteristics of the portfolio, including expected return, variance, and Sharpe ratio.
- **excel_handling.py**: Manages the exporting of results and data to an Excel file for easy viewing and manipulation.
- **LICENSE**: Licensing information for the project.
- **OPTIMAL_COMPLETE_PORTFOLIO_1.xlsx**: Example Excel file containing the results of an optimal portfolio analysis.

## Installation

To use this project, clone the repository and install the necessary Python packages:

```bash
git clone https://github.com/yourusername/optimal-complete-portfolio-establisher.git
cd optimal-complete-portfolio-establisher
pip install -r requirements.txt
```

## Usage

1. **Run the main script**: 
    ```bash
    python main.py
    ```
   This script will automatically pull data, perform portfolio optimization, and output the results.

2. **View Results**:
   The results of the portfolio optimization will be saved in an Excel file (`OPTIMAL_COMPLETE_PORTFOLIO_1.xlsx`) in the project directory.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or feedback, feel free to contact [Khoi Nguyen] at [nguyenanhkhoi0608@gmail.com].
