import pandas as pd
import numpy as np

def pairs_returns(prices, pair, window=252, entry_z=2.0, exit_z=0.0, stop_z=3.0):
    """
    Calculate the returns of a pairs trading strategy based on z-score signals.

    Args:
        prices (pd.DataFrame): Price data with assets as columns and datetime index.
        pair (tuple): Tuple of (asset1, asset2, beta) for the trading pair.
        window (int, optional): Rolling window size for z-score calculation. Default is 252.
        entry_z (float, optional): Z-score threshold to enter a trade. Default is 2.0.
        exit_z (float, optional): Z-score threshold to exit a trade. Default is 0.0.
        stop_z (float, optional): Z-score threshold for stop-loss. Default is 3.0.

    Returns:
        pd.Series: Time series of strategy returns for the given pair.
    """
    s1, s2, beta = pair
    price1, price2 = prices[s1], prices[s2]

    # Align and clean data
    price1 = price1.dropna()
    price2 = price2.dropna()
    common_idx = price1.index.intersection(price2.index)
    price1 = price1.loc[common_idx]
    price2 = price2.loc[common_idx]

    # Calculate spread and z-score
    spread = np.log(price1) - beta * np.log(price2)
    mean = spread.rolling(window).mean()
    std = spread.rolling(window).std()
    zscore = (spread - mean) / std

    position = pd.Series(0, index=spread.index)
    in_trade = False
    trade_type = 0  # 1 for long, -1 for short

    for t in range(window, len(spread)):
        if not in_trade:
            if zscore.iloc[t] > entry_z:
                position.iloc[t] = -1  # Short spread
                in_trade = True
                trade_type = -1
            elif zscore.iloc[t] < -entry_z:
                position.iloc[t] = 1   # Long spread
                in_trade = True
                trade_type = 1
        else:
            if (trade_type == 1 and zscore.iloc[t] >= exit_z) or \
               (trade_type == -1 and zscore.iloc[t] <= exit_z) or \
               (trade_type == 1 and zscore.iloc[t] < -stop_z) or \
               (trade_type == -1 and zscore.iloc[t] > stop_z):
                in_trade = False
                trade_type = 0
            else:
                position.iloc[t] = trade_type

    # Shift position to avoid lookahead bias
    position = position.shift().fillna(0)

    # Calculate returns
    ret1 = price1.pct_change()
    ret2 = price2.pct_change()
    returns = position * (ret1 - beta * ret2)
    returns = returns.fillna(0)
    returns.name = f"{s1}_{s2}"

    return returns
