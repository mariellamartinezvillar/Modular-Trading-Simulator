import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

def moving_average_strategy(data, short_window: int = 40, long_window: int = 100, use_ml: bool = True):
    """
    Generates moving average crossover signals.
    Includes optional ML-based prediction of next-day returns.
    """
    # 1. Initialize DataFrame
    signals = pd.DataFrame(index=data.index)
    signals["Close"] = data["Close"]

    # 2. Rule-Base Strategy
    signals["Short_MA"] = data["Close"].rolling(window=short_window, min_periods=1).mean()
    signals["Long_MA"] = data["Close"].rolling(window=long_window, min_periods=1).mean()

    signals["Signal"] = np.where(signals["Short_MA"] > signals["Long_MA"], 1, 0)
    signals["Position"] = signals["Signal"].diff().fillna(0)

    # 3. Returns for ML Target
    signals["Return"] = signals["Close"].pct_change()
    signals["Next_Return"] = signals["Return"].shift(-1)
    signals["Target"] = np.where(signals["Next_Return"] > 0, 1, 0)

    # 4. ML Feature Engineering
    signals["Ret_1"] = signals["Return"]
    signals["Ret_3"] = signals["Return"].rolling(window=3, min_periods=1).mean()
    signals["Ret_5"] = signals["Return"].rolling(window=5, min_periods=1).mean()

    feature_cols = ["Ret_1", "Ret_3", "Ret_5", "Short_MA", "Long_MA"]

    # Initialize ML outputs
    signals["ML_Signal"] = 0
    signals["ML_Confidence"] = 0.0

    # 5. ML Disable by User
    if not use_ml:
        return signals
    
    # 6. Prepare ML Dataset
    ml_data = signals.dropna(subset=feature_cols + ["Target"]).copy()

    if len(ml_data) < 50:
        # Not enough data to train a meaningful model
        return signals
    
    X = ml_data[feature_cols].values
    y = ml_data["Target"].values

    # Time-based split (no shuffling)
    split_idx = int(len(ml_data) * 0.7)
    X_train, y_train = X[:split_idx], y[:split_idx]

    # 7. Train Logistic Regression
    try:
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        # Predictions
        ml_data["ML_Pred"] = model.predict(X)
        ml_data["ML_Confidence"] = model.predict_proba(X)[:, 1]

        # Map predictions back to full DataFrame
        signals.loc[ml_data.index, "ML_Signal"] = ml_data["ML_Pred"]
        signals.loc[ml_data.index, "ML_Confidence"] = ml_data["ML_Confidence"]
        
        # Ensure clean types
        signals["ML_Signal"] = signals["ML_Signal"].astype(int)
        signals["ML_Confidence"] = signals["ML_Confidence"].astype(float)

    except Exception:
        # If anything goes wrong, ML stays disabled
        signals["ML_Signal"] = 0
        signals["ML_Confidence"] = 0.0
    
    return signals

    if short_window >= long_window:
        raise ValueError("Short window must be smaller than long window.")
    
    signals = pd.DataFrame(index=data.index)
    signals["Close"] = data["Close"]

    # --- Rule-based signals ---
    signals["Short_MA"] = data["Close"].rolling(window=short_window, min_periods=1).mean()
    signals["Long_MA"] = data["Close"].rolling(window=long_window, min_periods=1).mean()

    # Guarantee ML_Signal always exists
    signals['ML_Signal'] = 0

    signals["Signal"] = np.where(signals["Short_MA"] > signals["Long_MA"], 1, 0)

    #Detect position changes (buy/sell points)
    signals["Position"] = signals["Signal"].diff().fillna(0)

    # --- Returns (for ML target)
    signals["Return"] = signals["Close"].pct_change()
    signals["Next_Return"] = signals["Return"].shift(-1)

    # Binary target: 1 if next-day return > 0, else 0
    signals["Target"] = np.where(signals["Next_Return"] > 0, 1, 0)

    # --- Features for ML ---
    # Simple, fast features: recent returns and moving averages
    signals["Ret_1"] = signals["Return"]
    signals["Ret_3"] = signals["Return"].rolling(window=3, min_periods=1).mean()
    signals["Ret_5"] = signals["Return"].rolling(window=5, min_periods=1).mean()

    feature_cols = ["Ret_1", "Ret_3", "Ret_5", "Short_MA", "Long_MA"]

    # Drop rows with NaNs in features or target
    ml_data = signals.dropna(subset=feature_cols +["Target"]).copy()
    
    if len(ml_data) < 50:
        # Not enough data to train a meaningful model
        signals["ML_Signal"] = 0
        return signals
    
    X = ml_data[feature_cols].values
    y = ml_data["Target"].values

    # Time-based split: first 70% train, last 30% test
    split_idx = int(len(ml_data) * 0.7)
    X_train, y_train = X[:split_idx], y[:split_idx]

    # Train a simple logistic regression classifier
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Predict for all rows where features are available
    ml_data["ML_Pred"] = model.predict(X)

    # Initialize ML_Signal as 0 everywhere
    signals["ML_Signal"] = 0

    # Map predictions back to the original index
    signals.loc[ml_data.index, "ML_Signal"] = ml_data["ML_Pred"]
    
    # Ensure ML_Signal is int (0/1)
    signals["ML_Signal"] = signals["ML_Signal"].astype(int)

     # Validate signals
    if signals.empty:
        raise ValueError("No signals generated.\nCheck data integrity and window sizes.")

    return signals
    # Signal: 1 = buy, 0 = no position
    signals['Signal'] = 0
    signals.loc[signals['Short_MA'] > signals['Long_MA'], 'Signal'] = 1

    #Detect position changes (buy/sell points)
    signals['Position'] = signals['Signal'].diff()

    #Drop early rows with NaN values
    signals.dropna(inplace=True)

    # --- NumPy Returns ---
    signals['Returns'] = np.log(signals['Close'] / signals['Close'].shift(1))
    signals.dropna(inplace=True)

    # --- Scikit-learn Scaling ---
    scaler = StandardScaler()
    signals[['Short_MA', 'Long_MA', 'Returns']] = scaler.fit_transform(
        signals[['Short_MA', 'Long_MA', 'Returns']]
    )

    # --- PyTorch ML model ---
    model = SimpleSignalModel()

    # Prepare features for the model
    X = torch.tensor(
        signals[['Short_MA', 'Long_MA', 'Returns']].values,
        dtype=torch.float32
    )
    # Forward pass (no training, just inference)
    with torch.no_grad():
        ml_output = model(X).numpy().flatten()
    
    # Convert probabilities to binary signals    
    signals['ML_Signal'] = (ml_output > 0.5).astype(int)

    # Validate signals
    if signals.empty:
        raise ValueError("No signals generated.\nCheck data integrity and window sizes.")

    return signals
