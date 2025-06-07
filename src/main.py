import pandas as pd
import matplotlib.pyplot as plt
from data_loader import load_prices
from pairs_selection import find_cointegrated_pairs
from strategy import pairs_returns
from optimize_params import optimize_params

# Load historical price data
prices = load_prices("../data/price.csv")

# Identify cointegrated pairs
pairs = find_cointegrated_pairs(prices)
print(f"Selected pairs: {pairs}")

# Parameter grid for backtesting
param_grid = {
    'window': [60, 120, 252],
    'entry_z': [1.5, 2.0, 2.5],
    'exit_z': [0.0],
    'stop_z': [2.5, 3.0]
}

# Backtest to find best parameters for each pair
results = optimize_params(prices, pairs, param_grid, pairs_returns)
print("\nBest parameters for each pair:")
print(results.sort_values('cum_return', ascending=False))

# Compute returns for all pairs using their optimal parameters
all_returns = pd.DataFrame()
for _, row in results.iterrows():
    pair_name = row['pair']
    s1, s2 = pair_name.split('_')
    beta = [p for p in pairs if p[0] == s1 and p[1] == s2][0][2]
    pair = (s1, s2, beta)
    returns = pairs_returns(
        prices, pair,
        window=int(row['window']),
        entry_z=row['entry_z'],
        exit_z=row['exit_z'],
        stop_z=row['stop_z']
    )
    all_returns[pair_name] = returns

# Plot cumulative returns for each pair
plt.figure(figsize=(12, 6))
for col in all_returns.columns:
    series = all_returns[col]
    series = series[~series.index.duplicated(keep='first')].reset_index(drop=True)
    if getattr(series, "ndim", 1) != 1 or series.empty:
        continue
    plt.plot((1 + series).cumprod() - 1, label=str(col))
plt.title("Cumulative Returns for All Pairs (Best Params)")
plt.xlabel("Time")
plt.ylabel("Cumulative Returns")
plt.legend()
plt.grid(True)
plt.savefig("returns_per_pair.png")
plt.show()

# Plot aggregate cumulative return across all pairs
total_returns = all_returns.sum(axis=1)
plt.figure(figsize=(12, 6))
plt.plot((1 + total_returns).cumprod() - 1, label="Aggregate")
plt.title("Aggregate Cumulative Returns (Best Params)")
plt.xlabel("Time")
plt.ylabel("Cumulative Returns")
plt.legend()
plt.grid(True)
plt.savefig("total_returns.png")
plt.show()
