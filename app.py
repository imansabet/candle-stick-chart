from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime

yf.pdr_override()

# Prompt user for stock symbol, start date, and end date
symbol = input("Enter stock symbol: ")
start_date_str = input("Enter start date (YYYY-MM-DD): ")
end_date_str = input("Enter end date (YYYY-MM-DD): ")

# Convert input strings to datetime objects
try:
    startdate = datetime.strptime(start_date_str, "%Y-%m-%d")
    enddate = datetime.strptime(end_date_str, "%Y-%m-%d")
except ValueError as e:
    print("Error: could not parse date string. Details:", str(e))
    exit()

# Retrieve stock data from Yahoo Finance for specified dates
try:
    data = pdr.get_data_yahoo(symbol, start=startdate, end=enddate)
except Exception as e:
    print("Error retrieving data from Yahoo Finance:", str(e))
    exit()

# Define function to calculate increase/decrease status
def increase_decrease(close, open):
    if close > open:
        value = "Increase"
    elif close < open:
        value = "Decrease"
    else:
        value = "Equal"
    return value

# Add status, middle, and range columns to data
data["status"] = ["Increase" if c > o else "Decrease" if c < o else "Equal" for c, o in zip(data.Close, data.Open)]
data["middle"] = (data.Open + data.Close) / 2
data["range"] = abs(data.Open - data.Close)

# Create and display Bokeh candlestick chart
plot = figure(x_axis_type="datetime", width=800, height=400, sizing_mode="stretch_both")
plot.segment(data.index, data.High, data.index, data.Low, color="black")
plot.vbar(x=data.index[data["status"] == "Increase"], width=20*60*60*1000, top=data.Close[data["status"] == "Increase"], bottom=data.Open[data["status"] == "Increase"], fill_color="green", line_color="black")
plot.vbar(x=data.index[data["status"] == "Decrease"], width=20*60*60*1000, top=data.Open[data["status"] == "Decrease"], bottom=data.Close[data["status"] == "Decrease"], fill_color="red", line_color="black")

# Add tooltips
hover = HoverTool(
    tooltips=[
        ("Date", "@index{%F}"),
        ("Open", "@Open{$0.00}"),
        ("Close", "@Close{$0.00}"),
        ("High", "@High{$0.00}"),
        ("Low", "@Low{$0.00}"),
    ],
    formatters={"@index": "datetime"},
    mode="vline",
)
plot.add_tools(hover)

# Display chart in Jupyter notebook
output_file('candles.html')
show(plot)