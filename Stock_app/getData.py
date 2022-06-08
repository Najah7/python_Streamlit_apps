import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache 
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
 
        # 株価取得
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