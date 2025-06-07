import unittest
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.strategy import pairs_returns

class TestPairsTradingStrategy(unittest.TestCase):
    """
    Unit tests for the pairs trading strategy.

    Tests:
        - setUp: Initializes mock price data for two stocks.
        - test_pairs_returns_shape: Checks that the output of pairs_returns has the correct length.
        - test_pairs_returns_not_all_nan: Ensures that the returns contain non-NaN values after the rolling window.
    """
    def setUp(self):
        dates = pd.date_range(start="2020-01-01", periods=300)
        price1 = pd.Series(100 + np.cumsum(np.random.normal(0, 1, 300)), index=dates)
        price2 = pd.Series(100 + np.cumsum(np.random.normal(0, 1, 300)), index=dates)
        self.prices = pd.DataFrame({'A': price1, 'B': price2})

    def test_pairs_returns_shape(self):
        pair = ('A', 'B', 1.0)
        returns = pairs_returns(self.prices, pair, window=20)
        self.assertEqual(len(returns), len(self.prices))

    def test_pairs_returns_not_all_nan(self):
        pair = ('A', 'B', 1.0)
        returns = pairs_returns(self.prices, pair, window=20)
        self.assertTrue(returns[20:].notna().any())

if __name__ == '__main__':
    unittest.main()