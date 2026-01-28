import sqlite3

def save_portfolio_to_sql(portfolio, db_name="results.db"):
    """
    Saves the portfolio DataFrame to a SQLite database.
    """
    conn = sqlite3.connect(db_name)
    portfolio.to_sql("portfolio", conn, if_exists="replace", index=True)
    conn.close()