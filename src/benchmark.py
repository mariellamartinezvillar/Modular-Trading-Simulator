def buy_and_hold(data, signals_index, initial_capital=10000):
    """
    Buy-and-hold benchmark strategy.
    """
    # Align data to the exact dates used by the strategy
    aligned = data.loc[signals_index].copy()
    
    # Validate first price
    first_price = aligned['Close'].iloc[0]
    if first_price <= 0 or first_price is None:
        raise ValueError(f"Invalid first price for benchmark: {first_price}")
    
    # Compute number of shares purchased on day 1
    shares = initial_capital // first_price
    if shares == 0:
        raise ValueError(
            f"Initial capital ${initial_capital} is too small to buy 1 share at ${first_price}"
        )
    
    # Benchmark portfolio value over time
    benchmark = shares * aligned['Close']

    return benchmark