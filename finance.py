import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import seaborn as sns
import base64
import yfinance as yf
import urllib
import lxml  


st.title('S&P 500 App')
st.markdown("""This app retrieves the S&P 500 Table from wikipedia and its corresponding stock price data from Yahoo Finance""")
st.markdown("Data source: [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)")

st.sidebar.header('User Input Features')
#scrapping du tableu wikipedia

@st.cache_data
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    # Add a user aagent to avoid being blocked by Wikipedia
    headers = {"User-Agent": "Mozilla/5.0 "}
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req) as response:
        html = response.read()

    #extract the first table (S&P 500 company)
    df = pd.read_html(html, header=0)[0]
    return df
df = load_data()
st.write(df)
sectors = df.groupby('GICS Sector')

#sidebar sector selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique)

#Filtrer les données
df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]
st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + \
         ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')


#Yahoo finance
try:
    data = yf.download(tickers=list(df_selected_sector[:10].Symbol),
                    period='ytd',
                    interval='1d',
                    group_by='ticker',
                    auto_adjust=True,
                    )

except:
    print("No selected sector")


#plot closing price
def price_plot(symbol):
    df = pd.DataFrame(data[symbol]['Close'])
    df['Date'] = df.index
    plt.fill_between(df['Date'], df['Close'], color='skyblue')
    plt.plot(df['Date'], df['Close'], color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Closing Price', fontweight='bold')
    plt.ylabel('Date', fontweight='bold')
    return st.pyplot(plt)

num_company = st.sidebar.slider('Number of Companies', 1, 5)
if st.button('Show Plots'):
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)