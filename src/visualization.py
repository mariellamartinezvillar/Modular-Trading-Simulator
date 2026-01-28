import matplotlib.pyplot as plt

def plot_results(signals, portfolio, benchmark, ticker, show_ml=True, use_log_scale=False):
    # Safety check
    if show_ml and 'ML_Signal' not in signals.columns:
        print("Warning: ML_Signal column missing, skipping ML markers.")
        show_ml = False
        
    plt.style.use("seaborn-v0_8")

    # Two stacked plots, shared x-axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14,10), sharex=True)

    # --- Chart 1: Performance vs Benchmark ---
    ax1.plot(
        portfolio.index,
        portfolio['Total'],
        label='Equity Curve',
        color="blue",
        linewidth=2.5
    )

    ax1.plot(
        benchmark.index,
        benchmark.values,
        label="Buy & Hold",
        color="green",
        linewidth=2.5,
        alpha=0.9
    )
    ax1.set_ylabel("Equity Curve ($)", fontsize=12)
    ax1.legend(loc="upper left", fontsize=10, frameon=True)
    ax1.set_title(f"Strategy Performance vs Benchmark - {ticker}", 
                  fontsize=14, fontweight="bold")
    
    # Log scale
    if use_log_scale:
        ax1.set_yscale("log")
    
    # --- Chart 2: Price + Signals ---
    ax2.plot(
        signals.index,
        signals['Close'],
        label="Stock Price",
        color="saddlebrown",
        linewidth=1.2,
        alpha=0.85
    )

    # --- Rule-Based Signals ---
    buys = signals[signals['Position'] == 1]
    sells = signals[signals['Position'] == -1]

    ax2.scatter(
        buys.index,
        buys['Close'],
        color="limegreen",
        marker="^",
        s=70,
        alpha=0.9,
        label="Rule-Based Buy Signal",
        edgecolors="black",
        linewidths=0.6
    )
    ax2.scatter(
        sells.index,
        sells['Close'],
        color="red",
        marker="v",
        s=60,
        alpha=0.9,
        label="Rule-Based Sell Signal",
        edgecolors="black",
        linewidths=0.6
    )

    # --- ML Buy/Sell markers ---
    if show_ml:
        ml_buys = signals[(signals['ML_Signal'] == 1) & (signals["ML_Signal"].diff() == 1)]
        ml_sells = signals[(signals['ML_Signal'] == 0) & (signals["ML_Signal"].diff() == -1)]

        ax2.scatter(
            ml_buys.index,
            ml_buys['Close'],
            color="purple",
            marker="*",
            s=110,
            alpha=0.85,
            label="ML Buy Signal",
            edgecolors="white", 
            linewidths=0.8
        )

        ax2.scatter(
            ml_sells.index,
            ml_sells['Close'],
            color="black",
            marker="x",
            s=90,
            alpha=0.85,
            label="ML Sell Signal",
            linewidths=1.2
        ) 

    # --- ML Confidence Shading ---
    if "ML_Confidence" in signals.columns:
        ax3 = ax2.twinx()
        ax3.fill_between(
            signals.index,
            0,
            signals["ML_Confidence"],
            color="mediumpurple",
            alpha=0.3,
            label="ML Confidence"
        )
    ax3.set_ylim(0,1)
    ax3.set_ylabel("ML Confidence", fontsize=12)

    ax2.set_ylabel("Stock Price ($)", fontsize=12)
    ax2.legend(loc="upper left", fontsize=10, frameon=True, labelspacing=0.4)
    ax2.set_title(f"Trading Signals on Price Curve - {ticker}", 
                  fontsize=14, fontweight="bold")

    plt.tight_layout()
    plt.show()
    return fig, ax1, ax2

