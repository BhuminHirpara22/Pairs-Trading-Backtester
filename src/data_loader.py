import pandas as pd

def load_prices(filepath):
    """
    Load price data from a CSV file, set the first column as index (dates),
    parse dates, and drop columns with missing values.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Cleaned price data.
    """
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    df = df.dropna(axis=1)  # Remove columns with any missing values
    return df