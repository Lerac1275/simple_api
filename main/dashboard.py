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


# Wrapper functions to exploit caching functionality
@st.cache_data
def master_info_call(start_date, end_date, vs_currency:str='sgd'):
    return gk.get_all_coin_info(start_date=start_date, end_date=end_date, vs_currency=vs_currency, id_maps=id_maps)

@st.cache_data
def indiv_coin_info_call(coin_id, start_date, end_date, vs_currency:str='sgd'):
    return gk.get_coin_info(coin_id=coin_id, start_date=start_date, end_date=end_date, vs_currency=vs_currency)

@st.cache_data
def get_coin_ticker_ids():
    return gk.get_all_coin_info()

coin_info_df = get_coin_ticker_ids()

# Store tickers of all default coins
default_coins = list(id_maps.keys())
all_coins = default_coins

st.title('Crypto API dashboard')
st.subheader('Powered by coinGecko')

st.header("Coin ID & Date selection ")
st.text(f"These coins : {default_coins} are included by default.")
coin_id=st.text_input("Would you like to add another for comparison?")
start_date = st.date_input("Comparison start date", datetime.date(2021, 2, 1))
end_date = st.date_input("Comparison end date", datetime.date(2021, 7, 1))



# If this breaks then don't run anything else
if end_date < start_date:
    st.warning("Invalid interval range. The end date comes before the start date.", icon='⚠️')


else:
    # Extract all the data for the default coins
    master_dict = master_info_call(start_date=start_date, end_date=end_date)

    # See if there is a user-inputted coin
    if coin_id != '' :
        try :
            coin_ticker = coin_info_df.loc[coin_info_df['id']==coin_id, 'symbol'].to_list()[0].upper()
        except:
            st.warning("Provided coin_id does not exist in coinGecko database", icon='⚠️')
        
        # add it to the master dictionary and record it in the list of available tickers
        new_coin_df = indiv_coin_info_call(coin_id=coin_id, start_date=start_date, end_date=end_date)
        new_coin_df['coin'] = coin_ticker
        master_dict[coin_ticker] = new_coin_df
        all_coins.append(coin_ticker)




    # Main coin under examination
    main_coin = st.selectbox('Select main coin to examine', all_coins)
    # Display the dataframe with information for only the selected main coin
    main_coin_df = master_dict[main_coin]
    main_coin_df = main_coin_df.loc[:, main_coin_df.columns.difference(['coin'])]
    st.dataframe(main_coin_df, use_container_width=True)

    # Main chart for comparison & examination
    st.header("Comparison Chart")
    # Choose the metric
    metric = st.selectbox("Select comparison metric", ('prices_sgd', 'market_cap_sgd', 'total_volumes'))
    # Select which coins to compare across
    coin_selection = st.multiselect(
        label='Select coins for comparison'
        , options=all_coins
        , default=all_coins
    )
    comparison_chart = gp.plot_comp_metrics(master_dict=master_dict, metric=metric, coins=coin_selection)
    st.plotly_chart(comparison_chart, use_container_width=True)






