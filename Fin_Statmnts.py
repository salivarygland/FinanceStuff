''' Using Yahoo Finance to gather Balance Sheet data (Numbers are in thousands)'''

from lxml import html
import requests
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)

# Enter Stock Ticker Below or uncomment next line to allow user input
# symbol = input("NYSE Ticker? ")
symbol = 'V'


def get_page(url):
    # Set up the request headers that we're going to use, to simulate
    # a request by the Chrome browser. Simulating a request from a browser
    # is generally good practice when building a scraper
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    return requests.get(url, headers=headers)


def parsing(data_rows):
    parsed_rows = []

    for table_row in data_rows:
        parsed_row = []
        el = table_row.xpath("./div")

        none_count = 0

        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
            except ValueError:
                parsed_row.append(np.NaN)
                none_count += 1

        if none_count < 4:
            parsed_rows.append(parsed_row)

    return pd.DataFrame(parsed_rows)


def clean_data(df):
    df = df.set_index(0)
    df = df.transpose()
    cols = list(df.columns)
    cols[0] = 'Date'
    df = df.set_axis(cols, axis='columns', inplace=False)

    for column_index in range(1, len(df.columns)):
        df.iloc[:, column_index] = df.iloc[:, column_index].str.replace(',', '')  # Remove the thousands separator
        df.iloc[:, column_index] = df.iloc[:, column_index].astype(np.float64)  # Convert the column to float64

    return df


def scrape_table(url):
    page = get_page(url)
    tree = html.fromstring(page.content)

    # Fetch all div elements which have class 'D(tbr)'
    data_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

    assert len(data_rows) > 0

    df = parsing(data_rows)
    df = clean_data(df)

    return df


balance_sheet = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol)
#print(balance_sheet)

income_statement = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/financials?p=' + symbol)
print(income_statement)

cash_flow = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/cash-flow?p=' + symbol)
#print(cash_flow)

net_income = income_statement['Net Income Common Stockholders'][2]
print(net_income)

shares = income_statement['Basic Average Shares'][2]
print(shares)

EPS = net_income / shares
print("EPS in 2019: $", np.round(EPS, 2))
