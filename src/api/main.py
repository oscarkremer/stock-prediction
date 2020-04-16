from alpha_vantage.timeseries import TimeSeries

KEY = 'TSHI91Q1K43R9H5M'

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key=KEY, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='GOOG',interval='1min', outputsize='full')
data['1. open'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()