import pandas as pd

def backtest(signals, initial_capital=10000, trade_cost=5.0):
    """
    Simulates portfolio perfomance.
    """
    required_columns = {'Signal', 'Position', 'Close'}
    if not required_columns.issubset(signals.columns):
        raise ValueError(f"Signals DataFrame must contain the following columns: {required_columns}"
                         "\nCheck the strategy output.")
    
    #Ensure index alignment
    signals = signals.copy()
    signals.dropna(inplace=True)

    # Initialize portfolio DataFrame
    portfolio = pd.DataFrame(index=signals.index, dtype=float)
    portfolio['Cash'] = float(initial_capital)
    portfolio['Holdings'] = 0.0
    portfolio['Total'] = float(initial_capital)

    cash = initial_capital
    position = 0 # 0 = no position, > 0 = number of shares held
    
    for i in range(len(signals)):
        price = signals['Close'].iloc[i]
        trade_signal = signals['Position'].iloc[i]

        # BUY
        if trade_signal == 1:
            # buy as many shares as possible
            shares_to_buy = cash // price if price > 0 else 0
            if shares_to_buy > 0:
                cost = shares_to_buy * price + trade_cost
                cash -= cost
                position += shares_to_buy
        
        # SELL
        elif trade_signal == -1 and position > 0:
            proceeds = position * price - trade_cost
            cash += proceeds
            position = 0

        # Update portfolio values
        portfolio.iloc[i, portfolio.columns.get_loc('Holdings')] = position * price
        portfolio.iloc[i, portfolio.columns.get_loc('Cash')] = cash
        portfolio.iloc[i, portfolio.columns.get_loc('Total')] = cash + (position * price)

    return portfolio