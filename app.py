# Shiny app for displaying stock info

import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from shiny.express import input, render, ui

sns.set()

ui.panel_title("Finance Bro")

# Input for stock symbol and price how many days ago
ui.input_text("ticker_val", "Ticker Symbol", "aapl, nvda")
ui.input_numeric("days_ago", "Number of Days", 30)


@render.text
def text_val():
    """Loads stock data and displays stock price."""
    all_symbols = [i.strip() for i in input.ticker_val().split(",")]
    all_data = []
    for symbol in all_symbols:
        all_data.append(yf.download(symbol, period="5y"))
    stock_data = all_data[0]["Close"]
    stock_price = stock_data[-1 - int(input.days_ago())]
    return f"Closing  Price of {str.upper(all_symbols[0])} {input.days_ago()} Trading Days Ago: ${round(stock_price, 2)}"


@render.plot
def stock_chart():
    """Creates stock chart."""
    all_symbols = [i.strip() for i in input.ticker_val().split(",")]
    all_data = []
    for symbol in all_symbols:
        all_data.append(yf.download(symbol, period="5y"))
    plt.figure()
    stock_names = []
    for symbol, data in zip(all_symbols, all_data):
        stock_data = list(data["Close"])
        stock_names.append(yf.Ticker(symbol).info["longName"])
        stock_values = stock_data[-1 - input.days_ago() :]
        plt.plot(range(len(stock_values)), stock_values, label=symbol)
    plt.title(f"Stock Chart for {' and '.join(stock_names)}")
    plt.legend()
    step = max(int(input.days_ago() / 15), 1)
    stock_dates = [
        i.strftime("%Y-%m-%d") for i in all_data[0].index[-1 - input.days_ago() :]
    ][::step]
    plt.xticks(ticks=range(0, len(stock_values), step), labels=stock_dates, rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
