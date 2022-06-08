import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt
 
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
 

df = get_data(tickers=tickers, days=days)

companies = ['apple', 'meta']
data = df.loc[companies]

data.sort_index()
data = data.T.reset_index()
data.head()

data = pd.melt(data, id_vars=['Date']).rename(
    columns={'value':'Stock Prices(USD)'}
)

ymin, ymax = 250, 300

chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin,ymax])),
        color='Name:N'
    )
)


