import os
import pg8000
import requests
import logging

START_DATE = '2022-01-01'
logging.basicConfig(level=logging.INFO)


def get_stock_data():
    logging.info("Fetching data from Alpha vantage api")

    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    url = 'https://www.alphavantage.co/query'

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': 'AAPL',
        'outputsize': 'full',
        'apikey': api_key
    }

    response = requests.get(url, params=params)
    logging.info(f"Alpha vantage api response status code: {
                 response.status_code}")

    if response.status_code == 200:
        data = response.json()
        return data

    return None


def get_db_connection():
    logging.info("Establishing database connection")

    connection = pg8000.connect(
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('POSTGRES_DB')
    )

    logging.info("Database connection established")
    return connection


def backfill_two_years_data():
    data = get_stock_data('AAPL', START_DATE)

    # if no data is returned, exit the function
    if data is None:
        return

    # now we have the data, iterate over the data and insert it into the database
    daily_data = data.get('Time Series (Daily)', {})

    # filter all the data that is after the start date
    data_since_start_date = {}
    for date, values in daily_data.items():
        if date >= START_DATE:
            data_since_start_date[date] = values

    # iterate over the data and insert it into the database
    cursor = db_conn.cursor()
    db_conn = get_db_connection()

    # prepare the insert query
    insert_query = '''
        INSERT INTO aapl_stock_data (time, open_price, close_price, high_price, low_price, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''

    for date, values in data_since_start_date.items():
        # extract the required fields
        open_price = float(values.get('1. open', 0))
        high_price = float(values.get('2. high', 0))
        low_price = float(values.get('3. low', 0))
        close_price = float(values.get('4. close', 0))
        volume = int(values.get('5. volume', 0))

        # insert the data into the table
        cursor.execute(insert_query, (date, open_price,
                       close_price, high_price, low_price, volume))


if __name__ == '__main__':
    backfill_two_years_data()
