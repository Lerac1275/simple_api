from typing import Union
import pandas as pd
import plotly.express as px

def plot_comp_metrics(master_dict:dict, metric:str = 'prices_sgd', coins:list[str] = None) -> px.line:
    """
    Plots one of the three main metrics [prices, market_cap, volume]

    Inputs
    ------
    master_dict : dictionary
        Master dictionary containing all dataframes of the individual coins
    metric : str
        The metric to compare
    coins : list[str]
        The list of string coins to compare. If None then compare all coins in df

    Returns
    ------
    px.line
        A plotly express chart depicting the comparison of the selected metric
    """
    # Filter for the relevant coins if needed
    tdf = pd.DataFrame()
    for coin in coins:
        tdf = pd.concat([tdf, master_dict[coin]])
    if not coins:
        return px.line()
    fig = px.line(tdf, x="datetime", y=metric, color="coin"
                  , title = f"Graph of {metric}")
    return fig