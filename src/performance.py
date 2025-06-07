import matplotlib.pyplot as plt
import pandas as pd

def plot_cumulative_returns(returns):
    """
    Plots the cumulative returns over time.

    Parameters:
        returns (pd.Series): Series of periodic returns indexed by date.

    Displays:
        A matplotlib plot showing cumulative returns.
    """
    # Calculate cumulative returns from periodic returns
    cum_returns = (1 + returns).cumprod() - 1

    # Set up the plot
    plt.figure(figsize=(10,6))
    plt.plot(returns.index, cum_returns)  # Plot cumulative returns over time

    # Add title and axis labels
    plt.title("Cumulative Returns")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Returns")

    # Add grid for better readability
    plt.grid(True)

    # Display the plot
    plt.show()