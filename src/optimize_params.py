import numpy as np
import pandas as pd

def optimize_params(prices, pairs, param_grid, pairs_returns_func):
    """
    Grid-search backtest for pairs trading.

    Args:
        prices (pd.DataFrame): Price data.
        pairs (list of tuple): List of asset pairs.
        param_grid (dict): Parameter grid with keys 'window', 'entry_z', 'exit_z', 'stop_z'.
        pairs_returns_func (callable): Function to compute returns for a pair.

    Returns:
        pd.DataFrame: Best parameters and performance metrics for each pair.
    """
    results = []
    for pair in pairs:
        best = None
        best_cum_return = -np.inf
        # Iterate over all parameter combinations
        for window in param_grid['window']:
            for entry_z in param_grid['entry_z']:
                for exit_z in param_grid['exit_z']:
                    for stop_z in param_grid['stop_z']:
                        # Compute returns for current parameters
                        returns = pairs_returns_func(
                            prices, pair,
                            window=window,
                            entry_z=entry_z,
                            exit_z=exit_z,
                            stop_z=stop_z
                        )
                        cum_return = (1 + returns).cumprod().iloc[-1] - 1
                        sharpe = returns.mean() / (returns.std() + 1e-9) * np.sqrt(252)
                        # Track best result
                        if cum_return > best_cum_return:
                            best_cum_return = cum_return
                            best = {
                                'pair': f"{pair[0]}_{pair[1]}",
                                'window': window,
                                'entry_z': entry_z,
                                'exit_z': exit_z,
                                'stop_z': stop_z,
                                'cum_return': cum_return,
                                'sharpe': sharpe
                            }
        if best is not None:
            results.append(best)
    return pd.DataFrame(results)