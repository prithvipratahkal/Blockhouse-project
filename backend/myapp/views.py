from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from myapp.models import AaplStockData


# Create your views here.

@api_view(['GET'])
def back_test(request):
    """
    This function is used to back test the trading strategy
    """
    investing_amount = request.query_params.get('investing_amount', None)
    sell_period = request.query_params.get('sell_period', None)
    buy_period = request.query_params.get('buy_period', None)
    
    # if any of the parameters are missing, return a bad request response
    if investing_amount is None or sell_period is None or buy_period is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # if any of the parameters are not a number, return a bad request response
    if not investing_amount.isnumeric() or not sell_period.isnumeric() or not buy_period.isnumeric():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # if any of the parameters are less than 0, return a bad request response
    if int(investing_amount) < 0 or int(sell_period) < 0 or int(buy_period) < 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    stock_data = AaplStockData.get_data_with_moving_average(int(sell_period), int(buy_period))
    
    # sort the stock data by time
    stock_data = sorted(stock_data, key=lambda x: x.time)
    
    # iterate over the stock data and calculate the profit
    profit = 0
    buy = True
    amount_remaining = int(investing_amount)
    stocks_held = 0
    for stock in stock_data:
        if buy and stock.open_price < stock.buying_moving_average:
            stocks_held = int(amount_remaining) // stock.open_price
            amount_remaining = int(amount_remaining) % stock.open_price
            buy = False
        elif not buy and stock.close_price > stock.selling_moving_average:
            amount_remaining += int(stocks_held * stock.close_price)
            stocks_held = 0
            buy = True
    
    if stocks_held > 0:
        # sell the stocks at the last price
        amount_remaining += int(stocks_held * stock_data[-1].close_price)
    
    # return the profit
    profit = amount_remaining - int(investing_amount)
    return Response(status=status.HTTP_200_OK, data={'profit': profit})
