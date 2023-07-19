import streamlit as st
import pandas as pd
import datetime
import geckoAdmin as gk
import grapher as gp

# Collection of ticker to id mappings, obtained from searching the ticker with .search(query)
id_maps = {'ETH' : 'ethereum'
           , 'BTC' : 'bitcoin'
           , 'USDC' : 'usd-coin'
           , 'AXS' : 'axie-infinity'}


# Wrapper function to exploit caching functionality
@st.cache_data
def master_info_call(start_date, end_date, vs_currency:str='sgd'):
    return gk.get_all_coin_info(start_date=start_date, end_date=end_date, vs_currency=vs_currency, id_maps=id_maps)

st.title('Crypto API dashboard')
st.subheader('Powered by coinGecko')

start_date = st.date_input("Comparison start date", datetime.date(2021, 1, 1))
end_date = st.date_input("Comparison end date", datetime.date(2021, 1, 31))



# If this breaks then don't run anything else
if end_date < start_date:
    st.warning("Invalid interval range. The end date comes before the start date.", icon='⚠️')

else:
    # Extract all the data
    master_df = gk.get_all_coin_info(start_date=start_date, end_date=end_date)
    # Main coin under examination
    main_coin = st.selectbox('Select main coin to examine', list(id_maps.keys()))
    # Display the dataframe with information for only the selected main coin
    main_coin_df = master_df.loc[master_df['coin']==main_coin, master_df.columns.difference(['coin'])]
    st.dataframe(main_coin_df.style.highlight_max(subset = main_coin_df.columns.difference(['datetime']), axis=0)
                 , use_container_width=True, column_config={
                    #  Doesn't work because a styling object is passed instead of the actual dataframe numeric type
                     'prices_sgd' : st.column_config.NumberColumn(
                                    "Price (in SGD)",
                                    help="The coin price in SGD",
                                    format= "%d.2f"
                                )
                 })





