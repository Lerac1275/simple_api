import geckoAdmin as gk
import grapher as gp
import pandas as pd
import numpy as np
from datetime import datetime
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

class Test_geckoAdmin:
    id_maps = {'ETH' : 'ethereum'
           , 'BTC' : 'bitcoin'
           , 'USDC' : 'usd-coin'
           , 'AXS' : 'axie-infinity'}
    
    start= "01-01-2023"
    end= "01-06-2023"
    coin_id='ethereum'
    vs_currency='sgd'
    
    def test_api_call(self):
        """
        test that the api call works
        """
        result = cg.get_coin_market_chart_range_by_id(id=self.coin_id, from_timestamp=self.start, to_timestamp=self.end
                                                      , vs_currency=self.vs_currency)
        
        # Check the return object. This also checks that there was a valid response
        assert isinstance(result, dict)

    def test_coin_info_result(self):
        """
        This test checks that the API call wrapper & transformation works as expected
        """
        start= "01-01-2023"
        end= "01-06-2023"
        self.df = gk.get_coin_info(coin_id='ethereum', start_date=start, end_date=end)

        # Check the correctness of the return type
        assert isinstance(self.df, pd.DataFrame)
        # Check that the returned dataframe has the correct columns
        assert self.df.dtypes.to_list() == [np.dtype('<M8[ns]'), np.dtype('float64'), np.dtype('float64'), np.dtype('float64')]
        # Check that the api call has the dates as expected
        assert self.df.datetime.min() >= datetime.strptime(start,"%d-%m-%Y")
        assert self.df.datetime.max() <= datetime.strptime(end,"%d-%m-%Y")
    
    def test_collation(self):
        """
        This checks the the collation of individual coin dataframes worked
        """
        master_dict = gk.get_all_coin_info(start_date=self.start, end_date = self.end, vs_currency = self.vs_currency, id_maps = self.id_maps)

        # Check that there were 4 key entries
        assert len(list(master_dict.keys()))==4
        # Check that each was of the dataframe type
        assert list(map(lambda x : type(x), master_dict.values())) == [pd.DataFrame]*len(master_dict)
    
    def test_graphing(self):
        """
        This function tests that the graphing function works as intended
        """

        # Check the empty figure
        figure = gp.plot_comp_metrics(master_dict={}, coins=None)
        assert str(type(figure))== "<class 'plotly.graph_objs._figure.Figure'>"

        
    
