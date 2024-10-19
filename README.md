# StockWise

This project aims to develop a Django-based backend system for financial data analysis, with a focus on API integration, database management, and basic financial backtesting. The system will fetch daily stock data from Alpha Vantage and store it in a PostgreSQL database. With this historical data, users can test simple investment strategies to see how their decisions would have performed in the past. Additionally, the system integrates a pre-trained machine learning model to predict future stock prices, giving users both a look back at the past and a glimpse into potential future trends.

The goal is to create a straightforward, user-friendly system that focuses on three key areas:

- Building a robust Django application for API data handling.
- Providing a basic tool for backtesting investment strategies.
- Offering stock price predictions using an existing machine learning model.

## Installation

To set up the project locally, follow these steps:

<<<<<<< Updated upstream
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
=======
1. **Clone the repository:**

   ```bash
   git clone git@github.com:prithvipratahkal/Blockhouse-project.git
   cd Blockhouse
   ```

2. **Create and activate a virtual environment:**

   It's important to use a virtual environment to keep dependencies isolated.

   For Unix/macOS:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   For Windows:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install the required dependencies:**

   Once the virtual environment is activated, install the necessary libraries listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   If needed, migrate the database to set up the required tables:

   ```bash
   python manage.py migrate
   ```

5. **Run the project:**

   After completing the setup, you can run the Django development server:

   ```bash
   python manage.py runserver
   ```

## Setting up PostgreSQL in Docker

To set up a PostgreSQL instance using Docker, follow these steps:

1. **Run PostgreSQL in Docker**:
   
   Run the following command to start PostgreSQL and expose port 5432:

   ```bash
   docker run --name stock-closing-data -e POSTGRES_PASSWORD=<password> -p 5432:5432 -d postgres
   ```

2. **Connect to PostgreSQL and create a database**:

   After starting the container, connect to PostgreSQL using the following command:

   ```bash
   docker exec -it stock-closing-data psql -U postgres
   ```

   Once connected, create the database:
 
   ```sql
   CREATE DATABASE stock_closing_data;
   ```

Now you have a PostgreSQL or TimescaleDB instance running in Docker with a database named `stock_closing_data`.



## Database Schema for Stock Data

This section describes the schema used for storing daily stock data for Apple Inc. (AAPL) in a PostgreSQL database:

- **time**: A timestamp field that serves as the primary key for each record. It stores the date and time for when the stock data was recorded, mapped to PostgreSQL’s `TIMESTAMPTZ` type to handle time zones.
  
- **open_price**: A decimal field that captures the stock's opening price on the recorded day. This field is mapped to a `DECIMAL` type in PostgreSQL to ensure accuracy for financial data.
  
- **close_price**: A decimal field for the stock's closing price at the end of the day, also stored as a `DECIMAL` type.

- **high_price**: A decimal field representing the highest price the stock reached during the day, stored as `DECIMAL`.

- **low_price**: A decimal field representing the lowest price of the stock during the day, stored as `DECIMAL`.

- **volume**: A decimal field capturing the total trading volume for the stock on the recorded day. 

The schema is structured to ensure precise handling of financial data, and it is optimized for querying stock price trends and trading volumes over time. The table is named `aapl_stock_data` in the PostgreSQL database.
>>>>>>> Stashed changes
