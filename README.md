# StockWise

This project aims to develop a Django-based backend system for financial data analysis, with a focus on API integration, database management, and basic financial backtesting. The system will fetch daily stock data from Alpha Vantage and store it in a PostgreSQL database. With this historical data, users can test simple investment strategies to see how their decisions would have performed in the past. Additionally, the system integrates a pre-trained machine learning model to predict future stock prices, giving users both a look back at the past and a glimpse into potential future trends.

The goal is to create a straightforward, user-friendly system that focuses on three key areas:

- Building a robust Django application for API data handling.
- Providing a basic tool for backtesting investment strategies.
- Offering stock price predictions using an existing machine learning model.

## Installation

To set up the project locally, follow these steps:

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



## API Endpoints: 


### API Endpoint: `/api/backtest/`

This API endpoint allows users to simulate a simple trading strategy by backtesting historical stock data. The user provides specific parameters to guide the strategy, and the system uses historical data to calculate potential profit or loss based on those rules.

#### HTTP Method: `GET`

#### Query Parameters:
- **investing_amount** (required): The amount of money the user is investing in the stock (e.g., $1000). This parameter should be a positive numeric value representing the initial capital.
- **buy_period** (required): The moving average period (e.g., 50 days) used to determine when to buy the stock. The strategy will trigger a buy when the stock price dips below this average.
- **sell_period** (required): The moving average period (e.g., 200 days) used to determine when to sell the stock. The strategy will trigger a sell when the stock price rises above this average.

#### Functionality:
1. **Validate Input Parameters**: 
   - The API first checks whether the required query parameters (`investing_amount`, `buy_period`, and `sell_period`) are provided and are valid numeric values.
   - If any of these parameters are missing or invalid, the API returns a 400 Bad Request response with appropriate error messages.

2. **Fetch Historical Stock Data**:
   - The API retrieves historical stock price data for Apple Inc. (AAPL) from the database. This data includes close prices, open prices, and the relevant moving averages for each day.

3. **Simulate Trading Strategy**:
   - The backtesting logic simulates a trading strategy based on the user-provided buy and sell periods. The basic strategy is as follows:
     - Buy stock when the price falls below the buy period's moving average.
     - Sell stock when the price exceeds the sell period's moving average.
   - The system tracks when trades are made and calculates the profit or loss for each trade.

4. **Calculate Profit**:
   - After completing the simulation, the API calculates the overall profit (or loss) by comparing the final amount of money after all trades to the initial investing amount.

5. **Return Backtest Results**:
   - The API returns a JSON response that includes:
     - The total profit or loss from the backtest.

#### Response:
- **Status Code**: `200 OK`
- **Response Body**:
  - `profit`: The net profit or loss from the backtest.

#### Example Response:
```json
{
  "profit": 1200,
}
```

#### Workflow:
1. The user sends a GET request to `/api/backtest/` with the required query parameters (`investing_amount`, `buy_period`, and `sell_period`).
2. The API validates the inputs and performs the backtest using historical stock data.
3. The system calculates the profit or loss and returns a detailed summary of the trades that occurred during the backtest.


---

### API Endpoint: `/api/predict/`

This API endpoint provides predictions for future stock prices based on a pre-trained machine learning model. It forecasts the stock prices for the next 30 days using a linear regression model trained on historical data.

#### HTTP Method: `GET`

#### Functionality:
1. **Load Pre-trained Model**:
   - The API loads a pre-trained linear regression model from a file, which has been trained on historical stock price data. This model is used to predict the future stock prices.

2. **Fetch Historical Stock Data**:
   - The API retrieves the latest stock data from the database. This data includes the most recent close prices for the stock, which are used as input for the model.

3. **Prepare Data for Prediction**:
   - The API processes the historical stock data and reshapes it as required by the machine learning model. The last 30 days of stock prices are used as input to predict future prices.

4. **Generate Predictions**:
   - The linear regression model predicts stock prices for the next 30 days based on the input data.
   - The predicted stock prices are generated for each day over the next 30-day period.

5. **Return Predictions**:
   - The API returns a JSON response that includes:
     - The stock symbol (e.g., AAPL).
     - A list of predicted stock prices for the next 30 days, along with the corresponding dates.

#### Response:
- **Status Code**: `200 OK`
- **Response Body**:
  - `symbol`: The stock symbol for which predictions are made (e.g., AAPL).
  - `predictions`: A list of predicted stock prices for the next 30 days, along with the dates.

#### Example Response:
```json
{
  "symbol": "AAPL",
  "predictions": [
    {
            "date": "2024-10-19",
            "predicted_price": 168.79841595935096
        },
        {
            "date": "2024-10-20",
            "predicted_price": 168.56038644677184
        },
  ]
}
```

#### Workflow:
1. The user sends a GET request to `/api/predict/`.
2. The API retrieves the latest stock data and prepares it for the pre-trained model.
3. The model predicts the stock prices for the next 30 days, and the API returns these predictions in a structured JSON format.



### Public API Endpoint: `/api/prediction/report/`

This API generates a visual report comparing actual stock prices for the last 30 days with predicted prices for the next 30 days using a pre-trained linear regression model. The result is returned as a PNG image.

#### HTTP Method: `GET`

#### Functionality:
This endpoint provides users with a comprehensive visual report that includes both historical and predicted stock prices. The report includes the following steps:
1. **Load Pre-trained Model**:
   The API starts by loading a pre-trained linear regression model from a file to make stock price predictions.

2. **Fetch Latest Stock Data**:
   The API retrieves the most recent stock data from the database, including close prices and their corresponding timestamps. This data is used for both making predictions and plotting actual historical prices.

3. **Prepare Input Data for Prediction**:
   The API processes the stock data and prepares the last 30 days of close prices as input to the linear regression model.

4. **Predict Stock Prices for the Next 30 Days**:
   Using the pre-trained model, the API predicts the stock prices for the next 30 days based on the most recent historical data.

5. **Generate Prediction Dates**:
   The API generates dates for the next 30 days to correspond with the predicted stock prices.

6. **Plot the Actual and Predicted Prices**:
   - **Actual Prices**: Plotted for the last 30 days, shown in blue with circular markers.
   - **Predicted Prices**: Plotted for the upcoming 30 days, shown in green with dashed lines and cross markers.
   The plot provides a visual comparison between historical and predicted stock prices.

7. **Save Plot and Return as PNG**:
   The API generates a plot with labeled axes, a title, and a legend. The plot is then saved as a PNG image and returned as an HTTP response, allowing the user to view the visual report directly in their browser or download it.

#### Response:
- **Status Code**: `200 OK`
- **Content Type**: `image/png`
- The response contains the generated plot as an inline image.

#### Example Workflow:
1. The user sends a `GET` request to `/api/prediction/report/`.
2. The API retrieves the most recent 30 days of actual stock data from the database.
3. It applies the pre-trained model to predict stock prices for the next 30 days.
4. A visual report is generated, comparing the actual stock prices (last 30 days) and predicted stock prices (next 30 days).
5. The user receives a PNG image with a well-labeled plot, including:
   - Actual stock prices shown as a blue line with markers.
   - Predicted stock prices shown as a green dashed line with cross markers.
6. The plot helps users visualize the predicted trends in stock prices and compare them with recent historical data.

#### Description of Visual Plot:
- **X-Axis**: Represents the dates (both historical and predicted).
- **Y-Axis**: Represents the stock price in USD.
- **Actual Prices**: Displayed with a solid blue line for the last 30 days of stock data, using circular markers for each data point.
- **Predicted Prices**: Displayed with a dashed green line for the next 30 days, using cross markers to indicate predictions.
- **Title**: "Actual vs Predicted Stock Prices".
- **Legend**: Helps differentiate between actual and predicted prices.
- **Formatting**: The plot uses a clean format with rotated dates on the X-axis for better readability.

#### Example of the API Output (visualized):
When you call this endpoint, you’ll receive a visual comparison of how the stock has performed in the last 30 days and the predicted prices for the next 30 days, based on the model’s analysis.



## Backfill Stock Data on Server Initialization

The script(scripts/backfill_two_years_data.py) runs during the server initialization process and is designed to backfill stock data for the past two years into the database. It fetches historical stock data from the Alpha Vantage API and stores it in a PostgreSQL database using the `pg8000` driver. The script ensures that all data starting from a specific date (in this case, January 1, 2022) is fetched and saved into the database.

#### Functionality Overview

1. **Fetch Stock Data from Alpha Vantage API**:
   - The script interacts with the Alpha Vantage API to retrieve historical stock data for a specific symbol (AAPL in this case).
   - It uses the `TIME_SERIES_DAILY` function to get daily stock prices including the open, close, high, low, and volume data.
   - API requests are parameterized with the API key stored in environment variables for security.
   - The response from the API is parsed to extract the relevant stock data.

2. **Database Connection**:
   - The script establishes a connection to a PostgreSQL database using the `pg8000` library.
   - The database credentials, including the username, password, host, port, and database name, are retrieved from environment variables.
   - Once the connection is established, a cursor is created to execute SQL queries.

3. **Backfill Logic**:
   - The script iterates over the historical stock data and filters only the records from `2022-01-01` onwards.
   - It prepares an SQL `INSERT` query to store the stock data into the database.
   - For each valid date, it extracts the stock prices (open, close, high, low) and volume, and inserts the data into the `aapl_stock_data` table.
   - If any errors occur during data insertion, they are logged for debugging purposes.

4. **Data Commit and Cleanup**:
   - After all data has been inserted, the script commits the transaction to ensure that the changes are saved in the database.
   - Finally, the database cursor and connection are closed to release resources.

#### Key Components:

- **`get_stock_data()`**:
   - Fetches daily stock data for AAPL from the Alpha Vantage API.
   - Uses environment variables for the API key to ensure security.
   - Handles API responses and logs the status.

- **`get_db_connection()`**:
   - Establishes a connection to the PostgreSQL database using credentials from environment variables.
   - Logs the connection status and user details (excluding sensitive information).

- **`backfill_two_years_data()`**:
   - Handles the backfill process by:
     - Fetching stock data from the Alpha Vantage API.
     - Filtering data to only include records from `2022-01-01` onwards.
     - Preparing SQL queries to insert the data into the `aapl_stock_data` table.
     - Committing the transaction and logging any errors during the process.

#### Usage:

This script is executed when the server is initialized to ensure that the stock data table is pre-populated with the past two years of data.

```bash
# Command to run the script
python backfill_stock_data.py
```

Ensure that the following environment variables are set before running the script:

- `ALPHA_VANTAGE_API_KEY`: The API key for accessing Alpha Vantage.
- `POSTGRES_USER`: The username for PostgreSQL.
- `POSTGRES_PASSWORD`: The password for PostgreSQL.
- `POSTGRES_HOST`: The PostgreSQL host address.
- `POSTGRES_PORT`: The PostgreSQL port (default is 5432).
- `POSTGRES_DB`: The name of the database to connect to.

#### Example Log Output:

```
INFO:root:Fetching data from Alpha Vantage API
INFO:root:Alpha Vantage API response status code: 200
INFO:root:Establishing database connection
INFO:root:Database connection established
INFO:root:Inserting stock data for date: 2022-01-02, open_price: 150.25, close_price: 155.00, high_price: 157.00, low_price: 149.50, volume: 100000
INFO:root:Stock data inserted successfully
INFO:root:PostgreSQL connection closed.
```

This logging helps track the progress of data backfilling and provides useful information for debugging in case of any issues.


### Background Task: Daily Stock Data Update and Model Training

This background task is scheduled to run daily at midnight to update the stock data for the day and ensure that any missing data from previous days is backfilled. The task is implemented using the `apscheduler` library, which handles job scheduling in a Django-based environment.

#### Overview:

1. **Scheduler Initialization**:
   - The scheduler is initialized using `apscheduler.schedulers.background.BackgroundScheduler()`, which allows for jobs to run in the background without blocking other tasks.
   - Two main jobs are scheduled:
     - A daily task that updates the stock data at midnight.
     - A one-time task that trains a linear regression model at a specified time.

2. **Daily Stock Data Update**:
   - The task `update_latest_stock_data` is scheduled to run every day at **midnight (00:00)**. This task:
     - Fetches the stock data for the current day using the Alpha Vantage API.
     - Adds the new data to the database.
     - If there are any missing entries from previous days (e.g., due to server downtime), it backfills the database with the missing data.
   - This ensures that the stock data is always up-to-date, and any gaps in data collection are addressed automatically.

3. **Model Training**:
   - The task `train_linear_regression_model` is scheduled as a one-time job that runs at a specific time (`2024-10-19 09:56:00` in this case).
   - This task retrains the linear regression model on the latest stock data to ensure the model is using the most accurate information for future predictions.

4. **Logging**:
   - Logging is enabled to provide visibility into the task execution process. When the scheduler starts, a log entry is generated. Similarly, any issues during task execution are logged for debugging purposes.

#### Code Explanation:

```python
from apscheduler.schedulers.background import BackgroundScheduler
from myapp.tasks import update_latest_stock_data, train_linear_regression_model
from datetime import datetime
import logging

def start():
    scheduler = BackgroundScheduler()
    
    # Specific date and time for the model training task
    date_string = '2024-10-19 09:56:00'
    run_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    
    # Schedule the daily task to update stock data at midnight
    scheduler.add_job(update_latest_stock_data, 'cron', hour=0, minute=0) 
    
    # Schedule the model training task to run at the specified time
    scheduler.add_job(train_linear_regression_model, 'date', run_date=run_date) 
    
    # Start the scheduler
    scheduler.start()
    logging.info("Scheduler started")
```

#### Job Scheduling:

1. **`update_latest_stock_data`**:
   - Runs every day at midnight (00:00).
   - Fetches the stock data for the day and adds it to the PostgreSQL database.
   - Backfills any missing data for previous days that were not updated earlier.

2. **`train_linear_regression_model`**:
   - Runs once at the specified time (`2024-10-19 09:56:00`).
   - Retrains the linear regression model on the updated stock data, ensuring that the predictions for future stock prices are based on the most recent data.

#### Example of Scheduler Execution:

- At **midnight (00:00)**, the system automatically triggers the stock data update task. The task will:
   - Fetch the stock data for the current day.
   - Identify any missing data for previous days and fill those gaps.
   - Log each operation for transparency and debugging purposes.

- At the specified time (`2024-10-19 09:56:00`), the model training task runs and updates the linear regression model.

#### Logging Example:

```
INFO:root:Scheduler started
INFO:root:Stock data update task triggered for 2024-10-20
INFO:root:Stock data updated successfully for 2024-10-20
INFO:root:Missing data from 2024-10-18 filled successfully
INFO:root:Linear regression model training started at 2024-10-19 09:56:00
INFO:root:Model training completed successfully
```

#### Usage:

This task runs automatically in the background once the server starts. To start the scheduler, the following command is executed:

```bash
python manage.py runserver
```

Ensure that the appropriate environment variables and dependencies are set up for the scheduler to work correctly.

#### Environment Variables:

- `ALPHA_VANTAGE_API_KEY`: The API key for fetching stock data from Alpha Vantage.
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`: PostgreSQL credentials for accessing the database.

This scheduled task ensures that the stock data remains up-to-date and that the machine learning model is trained with the latest information, improving prediction accuracy over time.

