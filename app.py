import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from shiny.express import input, render, ui
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

#Input for stock symbol and price how many days ago
ui.input_text("ticker_val", "ticker symbol", "TXG")
ui.input_text("days_ago", "days ago", "0")

@render.text
def text_val():
    data = yf.download(input.ticker_val(), period="6mo") #Get more than 100 days of data
    stock_data = data['Close']
    stock_price = stock_data[-1-int(input.days_ago())]
    return f"Closing  Price {input.days_ago()} Trading Days Ago: {stock_price}"
