import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd


# 볼린저 밴드 값
def plot_bollinger_bands(data_list, n=20, k=2):
    columns = ['time', 'current', 'open', 'high', 'low', 'volume']
    df = pd.DataFrame(data_list, columns=columns)

    df["ma"] = df["current"].rolling(n).mean()
    df["std"] = df["current"].rolling(n).std()
    df["upperb"] = df["ma"] + (df["std"] * k)
    df["lowerb"] = df["ma"] - (df["std"] * k)
    df = df[n - 1:].copy()

    # col 생략 없이 출력
    pd.set_option('display.max_columns', None)
    print(df)

    return df


# 그래프로 만들기
def set_graph(df, n):
    plt.figure(figsize=(9, 5))
    plt.plot(df.index, df['current'], label='Close')
    plt.plot(df.index, df['upperb'], linestyle='dashed', label='Upper band')
    plt.plot(df.index, df['ma'], linestyle='dashed', label=f'Moving Average {n}')
    plt.plot(df.index, df['lowerb'], linestyle='dashed', label='Lower band')
    plt.legend(loc='best')
    plt.savefig('test.png')


def minites_bollinger_backtesting(item_code, minute_type, data_list, account):
    df = plot_bollinger_bands(data_list)
