import streamlit as st
import pandas as pd
import altair as alt
import getData  as gd

st.title("米国株価可視化アプリ")



st.sidebar.write("""
    #GAFA株価
    こちらは株価可視化ツールです。以下のオプションから表示日数を指定してください。
""")

st.sidebar.write("""
    ##表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
    ### 過去の**{days}日間**GAFA株価
""")


st.sidebar.write("""
    ##株価の範囲指定
""")

ymin, ymax = st.sidebar.slider(
    '範囲を指定してください', 0.0, 3500.0, (0.0, 3500.0)
)


tickers = {
    'apple': 'AAPL',
    'meta': 'FB',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
    'amazon': 'AMZN'
}

# yfinaceのデータ取得があるので例外に
try:
    df = gd.get_data(days, tickers)

    companies = st.multiselect(
                    '会社名を選択してください',
                    list(df.index),
                    ['google', 'amazon', 'meta', 'apple']
                )

    if not companies:
        st.error('少なくとも１社は選択してください')
    else:
        data = df.loc[companies]
        st.write(" ### 株価(USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value':'Stock Prices(USD)'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin,ymax])),
                color='Name:N'
            )
        )

        st.altair_chart(chart, use_container_width=True)
except:
    st.erro("""
        エラーが発生しました
    """)



