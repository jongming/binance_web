#from wsgiref.simple_server import demo_app
import numpy as np
import requests
import talib
import json
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import sys

key='7MPSS6H9U5E7U1YZ'

config = {
    "alpha_vantage": {
        "key": "7MPSS6H9U5E7U1YZ",
        "symbol": "IBM",
        "outputsize": "full",
        "key_adjusted_close": "5. adjusted close",
    },
    "data": {
        "window_size": 20,
        "train_split_size": 0.80,
    }, 
    "plots": {
        "xticks_interval": 90, # show a date every 90 days
        "color_actual": "#001f3f",
        "color_train": "#3D9970",
        "color_val": "#0074D9",
        "color_pred_train": "#3D9970",
        "color_pred_val": "#0074D9",
        "color_pred_test": "#FF4136",
    },
    "model": {
        "input_size": 1, # since we are only using 1 feature, close price
        "num_lstm_layers": 2,
        "lstm_size": 32,
        "dropout": 0.2,
    },
    "training": {
        "device": "cpu", # "cuda" or "cpu"
        "batch_size": 64,
        "num_epoch": 100,
        "learning_rate": 0.01,
        "scheduler_step_size": 40,
    }
}
def download_data(config):
    ts = TimeSeries(key=config["alpha_vantage"]["key"])
    data, meta_data = ts.get_daily(config["alpha_vantage"]["symbol"], outputsize=config["alpha_vantage"]["outputsize"])

    data_date = [date for date in data.keys()]
    data_date.reverse()

    data_close_price = [float(data[date][config["alpha_vantage"]["key_adjusted_close"]]) for date in data.keys()]
    data_close_price.reverse()
    data_close_price = np.array(data_close_price)

    num_data_points = len(data_date)
    display_date_range = "from " + data_date[0] + " to " + data_date[num_data_points-1]
    print("Number data points", num_data_points, display_date_range)

    return data_date, data_close_price, num_data_points, display_date_range

ts = TimeSeries(key=key, output_format='pandas')
data, meta_data = ts.get_daily(symbol='AAPL', outputsize='full')

print(data)

from pathlib import Path
filepath = Path('out.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
data.to_csv(filepath)
#data['4. close'].plot()
#plt.title('Daily MSFT stock')
#plt.show()
close = data['4. close'][::-1].to_numpy()
output = talib.SMA(close, timeperiod=14)

#print(close)
#rsi = talib.RSI(close)
#np.set_printoptions(threshold=sys.maxsize)
#print(rsi)