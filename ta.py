import numpy
import talib

close = numpy.random.random(100)


output = talib.SMA(close, timeperiod=10)
print(output)