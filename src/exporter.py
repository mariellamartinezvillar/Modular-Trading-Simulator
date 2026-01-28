import json

def save_results_to_json(portfolio, signals, filename="results.json"):
    """
    Saves the portfolio and signal data to a JSON file.
    """
    # Convert timestamps to string by resetting index and renaming index to Date
    portfolio_json = portfolio.reset_index().rename(columns={"index":"Date"})
    signals_json = signals.reset_index().rename(columns={"index":"Date"})

    # Ensure Data column is JSON-safe (string)
    portfolio_json["Date"] = portfolio_json["Date"].astype(str)
    signals_json["Date"] = signals_json["Date"].astype(str)
    
    data = {
        "portfolio": portfolio_json.to_dict(orient='list'),
        "signals": signals_json.to_dict(orient='list')
    }

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)