import yfinance as yf
from shiny.express import input, render, ui
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

ui.input_slider("val", "Stock Value ___ days ago:", min=0, max=250, value=50)
data = yf.download("TXG", period="1y")

@render.text
def slider_val():
    stock_data = data['Close']
    stock_price = stock_data[-1-input.val()]
    return f"Closing  Price {input.val()} Trading Days Ago: {stock_price}"

@render.plot
def stock_chart():
    stock_data = list(data['Close'])
    stock_values = stock_data[-1-input.val():]
    plt.plot(range(len(stock_values)), stock_values)
    plt.title(f"TXG Stock Price")
    step = max(int(input.val() / 15), 1)
    stock_dates = [i.strftime("%Y-%m-%d") for i in data.index[-1-input.val():]][::step]
    plt.xticks(ticks=range(0, len(stock_values), step), labels=stock_dates, rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
