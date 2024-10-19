# StockWise

This project aims to develop a Django-based backend system for financial data analysis, with a focus on API integration, database management, and basic financial backtesting. The system will fetch daily stock data from Alpha Vantage and store it in a PostgreSQL database. With this historical data, users can test simple investment strategies to see how their decisions would have performed in the past. Additionally, the system integrates a pre-trained machine learning model to predict future stock prices, giving users both a look back at the past and a glimpse into potential future trends.

The goal is to create a straightforward, user-friendly system that focuses on three key areas:

- Building a robust Django application for API data handling.
- Providing a basic tool for backtesting investment strategies.
- Offering stock price predictions using an existing machine learning model.

## Installation

To set up the project locally, follow these steps:

1) Clone the repository:
    ```
    git clone git@github.com:prithvipratahkal/Blockhouse-project.git
    cd Blockhouse
    ```

2) Create and activate a virtual environment:

   It's important to use a virtual environment to keep dependencies isolated.
    For Unix/macOS:

    ```
    python3 -m venv venv
    source venv/bin/activate
```
