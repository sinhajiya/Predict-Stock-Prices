#import all the libraries
import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
#functions

#1.load data
@st.cache_resource
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True) #put date in first column
    return data
st.set_page_config(
    page_title="Prediction",
)

#initalizing the dates
START ="2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Forecaste the Stock Prices for the Upcoming Years...")
st.write( """
            Using this tool, you can predict the future Opening And Closing Prices of the Stocks..\n
            However,keep in mind that this :red[JUST A PREDICTION] and the actual prices ought to differ....\n
            Select the Stock you want to analyze....\n
""")
stocks=("TATAMOTORS.NS","IREDA.NS","INFY.NS","VBL.NS","HCLTECH.NS")
selected_stocks=st.selectbox("Select Dataset to Predict....",stocks)

#loading data
data_load_state=st.text("Load data.....")
data = load_data(selected_stocks)
data_load_state.text("Loading data.....done!!")

#web_app
st.title("Stock Predication")
#radio for number of years
n_years=st.radio("Years of prediction:",(1,2,3,4))
period=n_years*365 #give number of days

#forecasting

#training data
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date":"ds","Close":"y"})

m=Prophet()
m.fit(df_train) #it will start training

#future dataframe
future = m.make_future_dataframe(periods=period)
forecast=m.predict(future)

st.subheader('Forecast Data') 
st.write(forecast.tail())

st.write('Forecast Data')
fig1=plot_plotly(m,forecast)
st.plotly_chart(fig1)
st.write('Forecast Components')
fig2=m.plot_components(forecast)
st.write(fig2)