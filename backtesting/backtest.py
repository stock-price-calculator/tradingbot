import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import constants
import view.backtest_view as view


class Kiwoom_BackTesting:

    def __init__(self, main_kiwoom):
        self.Kiwoom = main_kiwoom

    # 볼린저 밴드 값
    def plot_bollinger_bands(self, data_list, n=20, k=2):
        columns = ['time', 'current', 'open', 'high', 'low', 'volume']
        df = pd.DataFrame(data_list, columns=columns)

        df["ma"] = df["current"].rolling(n).mean()
        df["std"] = df["current"].rolling(n).std()
        df["upper"] = df["ma"] + (df["std"] * k)
        df["lower"] = df["ma"] - (df["std"] * k)
        df = df[n - 1:].copy()

        # # col 생략 없이 출력
        # pd.set_option('display.max_columns', None)
        # print(df)

        return df


    # 그래프로 만들기
    def set_graph(self,df, n):
        plt.figure(figsize=(9, 5))
        plt.plot(df.index, df['current'], label='Close')
        plt.plot(df.index, df['upper'], linestyle='dashed', label='Upper band')
        plt.plot(df.index, df['ma'], linestyle='dashed', label=f'Moving Average {n}')
        plt.plot(df.index, df['lower'], linestyle='dashed', label='Lower band')
        plt.legend(loc='best')
        plt.savefig('test.png')


    # 볼린저로만 테스트
    def bollinger_backtesting(self,item_code, time_type, data_list, target_per, target_sell_per):
        df = self.plot_bollinger_bands(data_list)

        buy_price = 0.0
        myasset = 10000
        buy = False

        # 총 손익
        asset = []

        per = 1
        count = 0  # 거래횟수
        win_count = 0  # 이득인 거래수

        target_per = 1.02
        target_sell_per = 0.982

        for i, row in df.iterrows():
            if count == 20:
                break;
            # 매수 조건 - 볼린저밴드 하단에 닿을 때
            if row['low'] <= row['lower'] and buy == False:
                buy = True
                count += 1
                buy_price = (int)(row['lower'] * 10) / 10.0
                myasset = (1 - constants.TRADE_CHARGE) * myasset  # 수수료
            elif buy == True and (row['high'] >= buy_price * target_per or
                                                         row['low'] <= buy_price * target_sell_per or
                                                         row['high'] >= row['upper']):
                if row['low'] <= buy_price * target_sell_per:
                    sell_price = buy_price * target_sell_per

                elif row['high'] >= row['upper']:
                    sell_price = (int)(row['upper'] * 10) / 10.0

                else:
                    sell_price = buy_price * target_per

                myasset = myasset * (1 + (sell_price - buy_price) / buy_price)
                myasset -= myasset * constants.TRADE_CHARGE

                asset.append(myasset)

                buy = False
                print(per)
                print(myasset)
                per = per * (1 + (sell_price - buy_price) / buy_price - constants.TRADE_CHARGE * 2)
                if sell_price - buy_price > 0:
                    win_count += 1
        view.bollinger_backtesting_result(item_code, time_type, per, myasset, count, win_count)
        # self.Kiwoom.return_list.append({
        #     "종목코드": item_code,
        #     "거래막대 타입": time_type,
        #     "퍼센트": per,
        #     "내자산": myasset,
        #     "거래 수": count,
        #     "이득": win_count,
        #     "손해" : count - win_count,
        # })
        #
        # self.Kiwoom.data_success = True
        # self.Kiwoom.continuous_data_success = True
        return {
            "종목코드": item_code,
            "거래막대 타입": time_type,
            "퍼센트": per,
            "내자산": myasset,
            "거래 수": count,
            "이득": win_count,
            "손해" : count - win_count,
        }


