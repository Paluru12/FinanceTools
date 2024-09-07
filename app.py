# Shiny app for displaying stock info

import pandas as pd
import plotly.express as px
import yfinance as yf
from shiny.express import input, render, ui
from shinywidgets import render_widget 

PERIOD = "max"

ui.panel_title("Finance Bro")

# Input for stock symbol and price how many days ago
ui.input_text("ticker_val", "Ticker Symbol(s)", "VOO", placeholder="AAPL, NVDA")
ui.input_numeric("days_ago", "Number of Trading Days", 30)
ui.input_checkbox("normalize", "Relative Growth")


def get_date(dates, days_ago):
    """Return the date <days_ago> trading days ago if it is within the range of dates."""
    try:
        return dates[-1-days_ago]
    except IndexError:
        return dates[0]


@render_widget
def plotly_stock_chart():
    """Creates stock chart."""
    all_symbols = [i.strip() for i in input.ticker_val().split(",")]
    all_data = []
    stock_names = [yf.Ticker(symbol).info["longName"] for symbol in all_symbols]
    #TODO: Convert this to one API call (pandas multi indices suck)
    for symbol in all_symbols:
        df = yf.download(symbol, period=PERIOD)
        df['Symbol'] = str.upper(symbol)
        from_date = get_date(df.index, input.days_ago())
        df = df.reset_index()
        df = df[df["Date"] >= from_date]
        if(input.normalize()):
            df['Close'] = 100 * (df['Close'] / float(df[df['Date'] == from_date]['Close'].iloc[0]) - 1)
        all_data.append(df)
    df = pd.concat(all_data)
    fig = px.line(
        df, x="Date", y="Close", color='Symbol'
    ).update_layout(
        title=f"Closing price of {' and '.join(stock_names)}",
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title="Relative Growth (%)" if input.normalize() else "Closing Price ($)"
    )
    return fig
