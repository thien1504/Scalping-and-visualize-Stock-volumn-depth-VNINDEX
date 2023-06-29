import requests
import bs4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

def convert_volume(s):
    s = float(s.replace(',',''))
    return s*10

def get_data(link):
    html = requests.get(link)
    soup = bs4.BeautifulSoup(html.text, 'lxml')
    price = [float(i.text) for i in soup.find_all('td', class_="Item_DateItem", rel="price")]
    volume = [i.text for i in soup.find_all('td', class_="Item_Price10", rel="volume")]
    volume = list(map(convert_volume, volume))
    d = {'Price': price, 'Volume': volume}
    df = pd.DataFrame(d)
    return df

def convert_date_and_month(i):
    if (i < 10):
        out = '0'+str(i)
    else:
        out = i
    return out

def volume_depth(stock_code, start_date, end_date):
    start_list = start_date.split('/')
    end_list = end_date.split('/')
    start_list = list(map(int, start_list))
    end_list = list(map(int, end_list))
    
    start_date = datetime.date(day=start_list[0], month=start_list[1], year=start_list[2])
    end_date = datetime.date(day=end_list[0], month=end_list[1], year=end_list[2])
    
    df = pd.DataFrame(columns=['Price','Volume'])
    
    for i in range((end_date - start_date).days):
        #print(f'Processing on {start_date.day}/{start_date.month}/{start_date.year}')
        y = get_data(f'https://s.cafef.vn/Lich-su-giao-dich-{stock_code}-6.chn?date={convert_date_and_month(start_date.day)}/{convert_date_and_month(start_date.month)}/{start_date.year}')
        start_date += datetime.timedelta(days=1)
        df = pd.concat([df,y])   
    
    print('Finish')
    output = df.groupby('Price').sum()
    
    return output

stock_code = input("Enter stock code:")
start_date = input("Start date :")
end_date = input("End date :")

df = volume_depth(stock_code, start_date, end_date)

df.plot(kind='bar', figsize=(20,8))
plt.title(f"{stock_code} volume depth from {start_date} to {end_date}")
plt.xlabel('Price')
plt.ylabel('Volume')
plt.show()