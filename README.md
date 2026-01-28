# Trading Strategy Backtester

A lightweight Python backtesting tool combining a Moving Average Crossover strategy with an optional ML-based signal. Built for clarity, experimentation, and fast iteration. 

## Features

- Historical data loading (Yahoo Finance)
- Moving Average Crossover strategy
- Optional ML signal (Logistic Regression)
- Portfolio backtesting with equity tracking
- Benchmark comparison (Buy & Hold)
- Dual-panel charts with ML confidence shading
- JSON + SQLite export
- Docker support
- Lightweight CI workflow

## Outputs

- **results.json** - signals + equity curve 
- **results.db** - SQLite version
- **Charts** - price, signals, ML confidence shading, benchmark 

## Strategy Overview

**Rule-Based:**
Buy when Short MA > Long MA, sell when Short MA < Long MA.

**ML-Based:**
Logistic Regression predicting whether next-day return will be positive.

Outputs:
- `ML_Signal` (0/1)
- `ML_Confidence` (0-1)