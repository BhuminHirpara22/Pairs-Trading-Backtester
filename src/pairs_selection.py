import numpy as np
import pandas as pd
import statsmodels.api as sm

def find_cointegrated_pairs(prices, corr_threshold=0.6, adf_pvalue=0.05):
    """
    Identify cointegrated pairs of assets based on price data.

    Args:
        prices (pd.DataFrame): DataFrame of asset prices (columns: assets, rows: dates).
        corr_threshold (float): Minimum correlation threshold for returns.
        adf_pvalue (float): Maximum p-value for ADF test to confirm cointegration.

    Returns:
        list: List of tuples (asset1, asset2, hedge_ratio) for cointegrated pairs.
    """
    pairs = []
    cols = prices.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            s1, s2 = cols[i], cols[j]
            # Calculate log prices and align indices
            log_a = np.log(prices[s1].dropna())
            log_b = np.log(prices[s2].dropna())
            common_idx = log_a.index.intersection(log_b.index)
            log_a = log_a.loc[common_idx]
            log_b = log_b.loc[common_idx]

            # Compute daily returns for correlation filter
            r1, r2 = log_a.diff().dropna(), log_b.diff().dropna()
            if len(r1) == 0 or len(r2) == 0:
                continue
            corr = np.corrcoef(r1, r2)[0, 1]
            if corr > corr_threshold:
                # Linear regression to estimate hedge ratio
                X = sm.add_constant(log_b)
                model = sm.OLS(log_a, X).fit()
                n = model.params[1]  # hedge ratio (slope)
                spread = log_a - n * log_b
                # Augmented Dickey-Fuller test for cointegration
                pval = sm.tsa.adfuller(spread)[1]
                if pval < adf_pvalue:
                    pairs.append((s1, s2, n))
    return pairs