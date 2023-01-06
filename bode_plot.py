import matplotlib.pyplot as plt
import pandas as pd

# Read data from file 'filename.csv'
dataf = pd.read_csv("csv/Book3.csv")

plt.xscale('log')
plt.plot(dataf['chan_1_freq'], dataf['DB'])
plt.show()