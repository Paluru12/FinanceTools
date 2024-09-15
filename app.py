# Shiny app for displaying stock info

import pandas as pd
import plotly.express as px
import yfinance as yf
from shiny import App, reactive, ui, render
from shinywidgets import render_widget, output_widget

PERIOD = "max"

def get_date(dates, days_ago):
    """Return the date <days_ago> trading days ago if it is within the range of dates."""
    try:
        return dates[-1-days_ago]
    except IndexError:
        return dates[0]
    
def get_news(symbol):
    return yf.Ticker(symbol).news

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Stock Chart",
        ui.layout_column_wrap(
            ui.input_text("ticker_val", "Ticker Symbol(s)", "MSFT, AAPL", placeholder="AAPL, NVDA"),
            ui.input_numeric("days_ago", "Number of Trading Days", 30, min=1)
        ),
        ui.input_checkbox("normalize", "Relative Growth"),
        ui.input_action_button("update", "Update"),
        output_widget("plotly_stock_chart"),
        ui.output_ui("make_news_table"),
    ),
    ui.nav_panel(
        "Portfolio",
    ),
    ui.nav_spacer(), 
    ui.nav_control(ui.input_dark_mode(id="light", mode="light")),
    title="Finance Bro",
)

def server(input, output, session):
    @render_widget
    @reactive.event(input.update, input.light, ignore_none=False)
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
            df, 
            x="Date", 
            y="Close", 
            color='Symbol', 
            template="plotly_white" if input.light() == 'light' else "plotly_dark"
        ).update_layout(
            title=f"Closing price of {' and '.join(stock_names)}",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Relative Growth (%)" if input.normalize() else "Closing Price ($)"
        )
        return fig
    
    @render.ui
    @reactive.event(input.update, ignore_none=False)
    def make_news_table():
        all_symbols = [str.upper(i.strip()) for i in input.ticker_val().split(",")]
        table = ui.navset_card_tab(
            *[
                ui.nav_panel(
                    symbol,
                    ui.accordion(
                        *[
                            ui.accordion_panel(
                                item["title"],
                                ui.tags.a("URL", href=item['link']), 
                                ui.br(), 
                                f"Publisher: {item['publisher']}",
                                ui.br(),
                                f"Published on {item['providerPublishTime']}"
                            ) 
                            for item in get_news(symbol)
                        ],
                        id=f"{symbol}_news",
                        open=False
                    )
                )
                for symbol in all_symbols
            ],
            title="News"
        )
        return table
        return ui.card(
            ui.card_header("News"),
            ui.card_body(table)
        )
    
app = App(app_ui, server)
