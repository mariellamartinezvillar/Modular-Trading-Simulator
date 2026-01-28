import sys, os
import matplotlib as plt
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_root, "src"))

from datetime import datetime
from data_loader import fetch_data
from strategy import moving_average_strategy
from backtester import backtest
from benchmark import buy_and_hold
from visualization import plot_results
from exporter import save_results_to_json
from database import save_portfolio_to_sql

def validate_inputs(ticker, start_date, end_date):
    if not ticker.strip():
        raise ValueError("Ticker cannot be empty.")
    
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if start >= end:
            raise ValueError("Start date must be before end date.")
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format.")
    
def parse_bool(bool_input):
    bool_input = bool_input.strip().lower() 
    if bool_input in ("true", "t", "yes", "y", "1"):
        return True
    if bool_input in ("false", "f", "no", "n", "0"):
        return False
    raise ValueError

def run_program():
    ticker = input("Enter stock ticker (e.g. AAPL): ").upper().strip()
    if not ticker.isalpha():
        raise ValueError("Ticker must only contain alphabetic characters.")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    validate_inputs(ticker, start_date, end_date)

    initial_capital = None
    while initial_capital is None:
        raw_input = input("Enter initial capital (e.g. 1000): ")

        # Clean the input
        cleaned = raw_input.replace("$", "").replace(",", ""). replace(" ", "").strip()

        try:
            value = float(cleaned)
            if value > 0:
                initial_capital = value
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number like 1000.")

    show_ml = None
    while show_ml is None:
        try:
            show_ml = parse_bool(input("Show ML signals? (True/False): "))
        except ValueError:
            print("Please enter True or False.")
    
    use_log_scale = None
    while use_log_scale is None:
        try:
            use_log_scale = parse_bool(input("Use Log Scale for Performance Chart? (True/False): "))
        except ValueError:
            print("Please enter True or False.")

    data = fetch_data(ticker, start_date, end_date)
    signals = moving_average_strategy(data, show_ml)
    portfolio = backtest(signals)
    benchmark = buy_and_hold(data, signals.index)

    fig, ax1, ax2 = plot_results(signals, portfolio, benchmark, ticker, show_ml, use_log_scale)

    # Save results
    save_results_to_json(portfolio, signals, "results.json")
    save_portfolio_to_sql(portfolio)
    
def main():
    while True:
        try:
            run_program()
            print("\nBacktest completed successfully.")
            break

        except ValueError as ve:
            print(f"\nError: {ve}\nPlease try again.")

        except Exception as e:
            print(f"\nAn Unexpected error (debug mode):")
            print(type(e).__name__, e)
            #print(f"\nAn unexpected error occurred\nPlease restart the program or check the code.")
            break

if __name__ == '__main__':
    main()
