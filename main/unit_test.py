import geckoAdmin as gk
import pandas as pd
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
        assert isinstance(result, dict)

    def test_coin_info_result(self):
        """
        This test checks that the API call wrapper & transformation works as expected
        """
        start= "01-01-2023"
        end= "01-06-2023"
        self.df = gk.get_coin_info(coin_id='ethereum', start_date=start, end_date=end)

        assert isinstance(self.df, pd.DataFrame)
        # Check that the api call has the dates as expected
        assert self.df.datetime.min() >= datetime.strptime(start,"%d-%m-%Y")
        assert self.df.datetime.max() <= datetime.strptime(end,"%d-%m-%Y")
    
    
