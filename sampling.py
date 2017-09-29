import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('input.csv')

print(data.head(3))

# Calculating the short-window moving average
short_rolling = data.rolling(window=3).mean()
print("\nshort-window moving average\n")
print (short_rolling.tail())
