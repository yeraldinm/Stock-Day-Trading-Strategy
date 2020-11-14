from zipline.api import symbol,order_target_percent,schedule_function, date_rules, time_rules,order
def initialize(context):
    # Define Symbol
    context.security = symbol('MSFT')
    # Define standard devation threshold
    context.std_dev_threshold = 0.6

    schedule_function(enter_position,
                      date_rule=date_rules.every_day(),
                      time_rule=time_rules.market_open())

    schedule_function(square_off,
                      date_rule=date_rules.every_day(),
                      time_rule=time_rules.market_close(minutes=1))


def enter_position(context, data):

    # Fetch 1 day data for the above security
    price = data.history(context.security, ['open', 'close'], 80, '1d')
    # Calculate today's open to previous day's close
    price['returns'] = (price['open'] - price['close'].shift(1)) / price['close'].shift(1)
    # Calculate standard deviation
    std_dev = price.returns.std()

    # Long Entry Position
    if price.returns[-1] > context.std_dev_threshold * std_dev:
        order(context.security, 50)
        print('Long Entry')

    # Short Entry Position
    if price.returns[-1] < -context.std_dev_threshold * std_dev:
        order(context.security, -50)
        print('Short Entry')

def square_off(context, data):
    # Exit Position
    order_target_percent(context.security, 0)
    print('Close Position')