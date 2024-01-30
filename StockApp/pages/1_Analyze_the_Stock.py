import plotly.express as px
import streamlit as st
import yfinance as yf
from datetime import date
import pandas as pd
from plotly import graph_objs as go

#1.load data
@st.cache_resource
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True) #put date in first column
    return data

#2.plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

START ="2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.set_page_config(
    page_title="Analyzation",
    )

st.title("Analyze the graphs from 2015 to present.....")

stocks=("TATAMOTORS.NS","IREDA.NS","INFY.NS","VBL.NS","HCLTECH.NS")
selected_stocks=st.selectbox("Select Dataset to Analyze..",stocks)

#loading data
data_load_state=st.text("Load data.....")
data = load_data(selected_stocks)
data_load_state.text("Loading data.....done!!")

#showing data
st.subheader('Raw Data')
st.write(data.tail())
plot_raw_data()
st.caption('Use the slider to change the time period')

st.subheader("Faceted Area Chart")
fig = px.area(stocks, x=data['Date'], y=data['Close'], labels={'Date':'Date', 'Close':'Closing Price'})
st.plotly_chart(fig)

