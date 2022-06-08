import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
 
days = 20
 
tickers = {
    'apple': 'AAPL',
    'meta': 'FB',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
    'amazon': 'AMZN'
 
}
 
def get_data(tickers, days):
    df = pd.DataFrame()
    for company in tickers.keys():
 
        # appleの株価取得
        tkr = yf.Ticker(tickers[company])
 
        # 情報を取得する日数
       
        hist = tkr.history(period=f'{days}d')
 
        #　日時の整形
        hist.index = hist.index.strftime('%d %B %Y')
 
        # カラム名の変更　Close → apple
        hist = hist[['Close']]
        hist.columns = [company]
 
        # 転置
        hist = hist.T
 
        # カラム名変更
        hist.index.name = 'Name'
 
        #データフレームにhistを追加
        df = pd.concat([df, hist])
 
    return df
 
#確認用
print(get_data(tickers=tickers, days=days))
