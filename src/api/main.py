from alpha_vantage.timeseries import TimeSeries

KEY = 'TSHI91Q1K43R9H5M'

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key=KEY, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
print(data)
#data['4. close'].plot()
#plt.title('Intraday Times Series for the MSFT stock (1 min)')
#plt.show()