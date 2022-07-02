from bs4 import BeautifulSoup
import requests
import pandas as pd
import altair as alt
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

def get_df_ec():
    url_ec = 'https://scraping.official.ec/'

    res_ec = requests.get(url_ec)
    soup = BeautifulSoup(res_ec.text, 'html.parser')

    item_list = soup.find('ul', {'id':'itemList'})

    items = item_list.find_all('li')

    data_ec = []
    for item in items:
        datum_ec = {}
        datum_ec['title'] = item.find('p',{'class':'items-grid_itemTitleText_5a0255a1'}).text
        price = item.find('p', {'class': 'items-grid_price_5a0255a1'}).text
        datum_ec['price'] = int(price.replace('¥', '').replace(',',''))
        datum_ec['link'] = item.find('a')['href']
        is_stock =item.find('p',{'class':'items-grid_soldOut_5a0255a1'}) == None
        datum_ec['is_stock'] = '在庫あり' if is_stock == True else '在庫なし'
        data_ec.append(datum_ec)

    df_ec = pd.DataFrame(data_ec)

    return df_ec

def get_worksheet():
    scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

    credentials = Credentials.from_service_account_file(
            'api_key.json',
            scopes=scopes
        )

    gc = gspread.authorize(credentials)


    SP_SHHET_KEY = '1RPKAttvqfzZL1ChrM2cTmKWpfyzhKj-IWLV-DLJCUEM'
    sh = gc.open_by_key(SP_SHHET_KEY)

    SP_SHHET = 'db'
    worksheet = sh.worksheet(SP_SHHET)

    return worksheet

def get_chart():
    worksheet = get_worksheet()

    data = worksheet.get_all_values()

    df_udemy = pd.DataFrame(data[1:], columns=data[0])

    df_udemy = df_udemy.astype({
        'n_subscriber':int,
        'n_review':int,
    })

    y_min1 = df_udemy['n_subscriber'].min() - 10
    y_max1 = df_udemy['n_subscriber'].max() + 10

    y_min2 = df_udemy['n_review'].min() - 10
    y_max2 = df_udemy['n_review'].max() + 10


    base = alt.Chart(df_udemy).encode(
        alt.X('date:T', axis=alt.Axis(title=None))
    )

    line1 = base.mark_line(opacity=0.3, color='#57A44C').encode(
        alt.Y('n_subscriber',
            axis=alt.Axis(title='受講生数', titleColor='#57A44C'),
            scale=alt.Scale(domain=[y_min1, y_max1]))
    )

    line2 = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
        alt.Y('n_review',
            axis=alt.Axis(title='レビュー数', titleColor='#5276A7'),
            scale=alt.Scale(domain=[y_min2, y_max2]))
    )

    chart = alt.layer(line1, line2).resolve_scale(
    y = 'independent'
    )
    return chart

df_ec = get_df_ec()
chart = get_chart()

st.title('Webスクレイピング活用アプリ')

st.write('## Udemy情報')
st.altair_chart(chart, use_container_width=True)

st.write('## EC在庫情報', df_ec)