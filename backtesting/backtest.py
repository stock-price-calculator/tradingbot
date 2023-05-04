import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd


def plot_bollinger_bands(data_list, n=20, k=2):
    columns = ['time', 'current', 'open', 'high', 'low', 'volume']
    df = pd.DataFrame(data_list, columns=columns)

    print(df)

    df["ma"] = df["current"].rolling(n).mean()
    df["std"] = df["current"].rolling(n).std()
    df["upperb"] = df["ma"] + (df["std"] * k)
    df["lowerb"] = df["ma"] - (df["std"] * k)
    df = df[n - 1:].copy()

    plt.figure(figsize=(9, 5))
    plt.plot(df.index, df['current'], label='Close')
    plt.plot(df.index, df['upperb'], linestyle='dashed', label='Upper band')
    plt.plot(df.index, df['ma'], linestyle='dashed', label=f'Moving Average {n}')
    plt.plot(df.index, df['lowerb'], linestyle='dashed', label='Lower band')
    plt.legend(loc='best')
    plt.savefig('test.png')
def minites_backtesting(data_list):
    columns = ['time', 'current', 'open', 'high', 'low', 'volume']
    df = pd.DataFrame(data_list, columns=columns)

    df['ma'] = df['current'].rolling(20).mean()
    df["std"] = df["current"].rolling(20).std()
    df["upperb"] = df["ma"] + (df["std"] * 2)
    df["lowerb"] = df["ma"] - (df["std"] * 2)

    plt.style.use('seaborn')
    plt.figure(figsize=(20, 10))
    plt.style.use('seaborn')
    df[["upperb", "current", "ma", "lowerb"]].plot(ax=plt.gca())
    plt.fill_between(df.index, df.lowerb, df.upperb, color="b", alpha=0.1)
    plt.savefig('test.png')



