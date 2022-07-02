from bs4 import BeautifulSoup
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import datetime
from gspread_dataframe import set_with_dataframe



def get_data_udemy():
    url ='https://scraping-for-beginner.herokuapp.com/udemy'

    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    n_subscriber = soup.find('p',{'class':'subscribers'}).text
    n_subscriber = int(n_subscriber.split('：')[1])

    n_review = soup.find('p',{'class':'reviews'}).text
    n_review = int(n_review.split('：')[1])

    return {
        'n_subscriber':n_subscriber,
        'n_review': n_review,
    }


def main():
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
    data = worksheet.get_all_values()

    df = pd.DataFrame(data[1:], columns=data[0])

    df_udemy = get_data_udemy()
    today = datetime.date.today().strftime('%Y/%m/%d')

    df_udemy['date'] = today
    df.append(df_udemy, ignore_index=True)

    set_with_dataframe(worksheet, df, row=1, col=1)

if __name__ == '__main__':
    main()