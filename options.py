# Options Calculator
# calculates break even stock prices, maximum profit and loss

def get_options():
    """Get a list of option objects through user input"""
    options = []
    counter = 1
    while True:
        temp_option = {}
        prompt = f"Enter the details for option {counter}, or enter q at anytime to finish: "
        print(prompt)

        while True:
            position = input('Enter buy or sell: ')
            if position == 'buy' or position == 'sell' or position == 'q':
                break
        if position == 'q':
            break
        temp_option['position'] = position

        while True:
            type = input('Enter call or put: ')
            if type == 'call' or type == 'put' or type == 'q':
                break
        if type == 'q':
            break
        temp_option['type'] = type

        while True:
            strike = input('Enter the strike price: ')
            if strike == 'q':
                break
            try:
                strike = int(float(strike)*100)
            except ValueError:
                pass
            else:
                break
        if strike == 'q':
            break
        temp_option['strike'] = strike

        while True:
            price = input('Enter the option price: ')
            if price == 'q':
                break
            try:
                price = int(float(price)*100)
            except ValueError:
                pass
            else:
                break
        if price == 'q':
            break
        temp_option['price'] = price

        options.append(temp_option)
        counter += 1

    return options

def lowest_strike(options):
    """Find and return the lowest strike price in a list of options."""
    lowest_strike_price = options[0]['strike']
    for option in options:
        if option['strike'] < lowest_strike_price:
            lowest_strike_price = option['strike']
    return lowest_strike_price

def highest_strike(options):
    """Find and return the highest strike price in a list of options."""
    highest_strike_price = options[0]['strike']
    for option in options:
        if option['strike'] > highest_strike_price:
            highest_strike_price = option['strike']
    return highest_strike_price

def get_profit_at_stock_price(option, stock_price):
    """Find and return the profitability of an option at a stock price."""
    # if long
    if option['position'] == 'buy':
        cost = option['price'] * 100
        # if long on call
        if option['type'] == 'call':
            revenue = stock_price - option['strike']
            revenue *= 100
            if revenue < 0:
                revenue = 0
        # if long on put
        else:
            revenue = option['strike'] - stock_price
            revenue *= 100
            if revenue < 0:
                revenue = 0
        return revenue - cost
    # if short
    else:
        revenue = option['price'] * 100
        # if short on call
        if option['type'] == 'call':
            cost = stock_price - option['strike']
            cost *= 100
            if cost < 0:
                cost = 0
        # if short on put
        else:
            cost = option['strike'] - stock_price
            cost *= 100
            if cost < 0:
                cost = 0
        return revenue - cost

def get_total_profit_at_stock_price(options, stock_price):
    """Find and return the total profit for a list of options at a stock price."""
    profit = 0
    for option in options:
        profit += get_profit_at_stock_price(option, stock_price)
    return profit

def get_max_profit(options):
    if get_total_profit_at_stock_price(options, highest_strike(options)) < get_total_profit_at_stock_price(options, highest_strike(options)+1):
        return 'infinite'
    elif get_total_profit_at_stock_price(options, lowest_strike(options)) < get_total_profit_at_stock_price(options, lowest_strike(options)-1):
        return 'infinite'

    profits = []
    profits.append(get_total_profit_at_stock_price(options, 0))
    for option in options:
        profits.append(get_total_profit_at_stock_price(options, option['strike']))
    return max(profits)/100

def get_max_loss(options):
    if get_total_profit_at_stock_price(options, highest_strike(options)) > get_total_profit_at_stock_price(options, highest_strike(options)+1):
        for option in options:
            print(f"Profit at price {highest_strike(options)} = {get_profit_at_stock_price(option, highest_strike(options))}")
            print(f"Profit at price {highest_strike(options)+1} = {get_profit_at_stock_price(option, highest_strike(options)+1)}")

        print("1")
        return 'infinite'
    elif get_total_profit_at_stock_price(options, lowest_strike(options)) > get_total_profit_at_stock_price(options, lowest_strike(options)-1):
        print("2")
        return 'infinite'

    profits = []
    profits.append(get_total_profit_at_stock_price(options, 0))
    for option in options:
        profits.append(get_total_profit_at_stock_price(options, option['strike']))
    return min(profits)/100

def get_break_even_endpoint(options, endpoint):
    if endpoint == 'low':
        step = -1
    else:
        step = 1
    price = lowest_strike(options)
    while True:
        total_profit = get_total_profit_at_stock_price(options, price)
        if total_profit < 1 and total_profit > -1:
            return price
        price = price + step

def get_break_even_points(options):
    #check endpoints: if slope positive and profit negative, iterate up to find be. if slope negative and profit positive, iterate down to find be. Then also check full range.
    break_even_points = []

    low = get_total_profit_at_stock_price(options, lowest_strike(options))
    high = get_total_profit_at_stock_price(options, highest_strike(options))
    low_slope = low - get_total_profit_at_stock_price(options, lowest_strike(options)-1)
    high_slope = get_total_profit_at_stock_price(options, highest_strike(options)+1) - high

    if (low < 0 and low_slope < 0) or (low > 0 and low_slope > 0):
        break_even_points.append(get_break_even_endpoint(options, 'low'))
    if (high < 0 and high_slope > 0) or (high > 0 and high_slope < 0):
        break_even_points.append(get_break_even_endpoint(options, 'high'))
    price = lowest_strike(options)
    max_price = highest_strike(options)
    while price < max_price:
        total_profit = get_total_profit_at_stock_price(options, price)
        if total_profit < 1 and total_profit > -1:
            break_even_points.append(price)
        price = price + 1
    return set(break_even_points)

options = get_options()
if options:
    print(f"The max profit is ${get_max_profit(options)}")
    print(f"The max loss is ${(get_max_loss(options))}")
    be_points = get_break_even_points(options)
    print(f"The break even points are: ")
    for point in be_points:
        print(f"${point/100}")
