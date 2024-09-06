import yfinance as yf
from shiny.express import input, render, ui
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

ui.panel_title("Finance Bro")

#Input for stock symbol and price how many days ago
ui.input_text("ticker_val", "Ticker Symbol", "TXG")
ui.input_numeric("days_ago", "days ago", 30)
data = yf.download("TXG", period="5y")

@render.text
def text_val():
    global data
    data = yf.download(input.ticker_val(), period="5y")
    stock_data = data['Close']
    stock_price = stock_data[-1-int(input.days_ago())]
    return f"Closing  Price {input.days_ago()} Trading Days Ago: ${round(stock_price, 2)}"

@render.plot
def stock_chart():
    stock_data = list(data['Close'])
    stock_name = yf.Ticker(input.ticker_val()).info['longName']
    stock_values = stock_data[-1-input.days_ago():]
    plt.plot(range(len(stock_values)), stock_values)
    plt.title(f"{stock_name} Stock Price")
    step = max(int(input.days_ago() / 15), 1)
    stock_dates = [i.strftime("%Y-%m-%d") for i in data.index[-1-input.days_ago():]][::step]
    plt.xticks(ticks=range(0, len(stock_values), step), labels=stock_dates, rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
