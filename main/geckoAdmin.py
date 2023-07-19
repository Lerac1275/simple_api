from typing import Union
import pandas as pd
from datetime import datetime
import time 

# Collection of ticker to id mappings, obtained from searching the ticker with .search(query)
# Mapping in the form {"symbol/ticker : coin_id"}
id_maps = {'ETH' : 'ethereum'
           , 'BTC' : 'bitcoin'
           , 'USDC' : 'usd-coin'
           , 'AXS' : 'axie-infinity'}

from pycoingecko import CoinGeckoAPI
gk = CoinGeckoAPI()

def clean_market_chart_range(input_dict:dict) -> pd.DataFrame:
    """
    This function converts the API response of a call to obtain historic market values for a selected cryptocurrency to a pandas dataframe

    Input
    -----
    input_dict : dictionary
        Returned json dictionary object from the API call. Expected to have used get_coin_market_chart_range_by_id()
    
    Output
    ------
    pd.DataFrame
        Dataframe with relevant information as outlined in the problem statement
    """
    intervals = map(lambda x : x[0], input_dict['prices'])
    prices = map(lambda x : x[1], input_dict['prices'])
    market_cap = map(lambda x : x[1], input_dict['market_caps'])
    volumes = map(lambda x : x[1], input_dict['total_volumes'])

    result = pd.DataFrame({'datetime' : intervals
                        , 'prices_sgd' : prices
                        , 'market_cap_sgd' : market_cap
                        , "total_volumes" : volumes})
    
    result['datetime'] = pd.to_datetime(result['datetime'],unit='ms')

    return result

def get_coin_info(coin_id:str, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date], vs_currency:str='sgd') -> pd.DataFrame:
    """
    Main function that obtains the dataframe representation of the historic information of a given coin for a selected interval period. 
    """
    # Convert the start & end dates to unix timestamps
    if type(start_date)==str:
        start_date = datetime.strptime(start_date,"%d-%m-%Y")
    start_date=time.mktime(start_date.timetuple())

    if type(end_date)==str:
        end_date = datetime.strptime(end_date,"%d-%m-%Y")
    end_date=time.mktime(end_date.timetuple())

    # Make the api request
    result=gk.get_coin_market_chart_range_by_id(id=coin_id, from_timestamp=start_date, to_timestamp=end_date, vs_currency=vs_currency)

    # Convert it to the desired pandas dataframe format
    result = clean_market_chart_range(result)
    return result

def get_all_coin_info(start_date : Union[str, datetime.date], end_date : Union[str, datetime.date], vs_currency:str='sgd', id_maps = id_maps) -> pd.DataFrame:
    """
    Function to consolidate records from ALL 4 examined coin types. Used to speed up comparison aggregation later on
    """
    # final = pd.DataFrame()
    result = {}
    for ticker, id_name in id_maps.items():
        # Get the coin information for the selected time period
        tdf = get_coin_info(coin_id=id_name, start_date=start_date, end_date=end_date, vs_currency=vs_currency)
        # Attach the ticker name
        tdf['coin'] = ticker
        # Append to result
        result[ticker]=tdf
    # Return the final dataframe containing info for all coins
    return result

def get_all_coin_info():
    return pd.DataFrame(gk.get_coins_list())