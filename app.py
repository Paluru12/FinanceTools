import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from shiny.express import input, render, ui
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

ui.input_slider("val", "Stock Value ___ days ago:", min=0, max=150, value=0)

@render.text
def slider_val():
    data = yf.download("TXG", period="6mo") #Get more than 100 days of data
    #day = (datetime.today() - timedelta(days=input.val())).strftime("%Y-%m-%d")
    #stock_price = data.loc[day]["Close"]
    stock_data = data['Close']
    stock_price = stock_data[-1-input.val()]
    return f"Closing  Price {input.val()} Trading Days Ago: {stock_price}"