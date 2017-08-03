from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from csv import writer


SOURCE = 'https://coinmarketcap.com/all/views/all/'

coins_dict = {}

page = get(SOURCE)
c = page.content
soup = BeautifulSoup(c, 'html5lib')
tr_tags = soup.find_all('tr')
for i in range(1, len(tr_tags)):
    tr_split = tr_tags[i].text.split('\n')
    tr_strip = [s.lstrip() for s in tr_split]

    # coin_data = filter(None, tr_strip)        # <---- Python 2
    coin_data = list(filter(None, tr_strip))  # <---- Python 3

    market_cap_rank = coin_data[0]
    name = coin_data[1]
    symbol = coin_data[2]
    market_cap = coin_data[3]
    price = coin_data[4]
    circulating_supply = coin_data[5]
    volume = coin_data[6]
    hour_percent_d = coin_data[7]
    day_percent_d = coin_data[8]
    week_percent_d = coin_data[9]
    coins_dict[symbol] = [market_cap_rank, name, market_cap, price, circulating_supply, volume, hour_percent_d, day_percent_d, week_percent_d]

utc_time = datetime.now(timezone('UTC')).strftime("%Y%m%d-%H%M%S")
filename = '/home/ubuntu/crypt_15/crypt_15_min/data/cr_' + utc_time + '.csv'

with open(filename, 'w+') as csv_file:
    csv_writer = writer(csv_file)
    csv_writer.writerow(['symbol', 'ranking by market cap', 'name', 'market cap', 'price', 'circulating supply', 'volume', '% 1h', '% 24h', '% 1wk'])
    for key, value in coins_dict.items():
        csv_writer.writerow([key, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8]])

print('cr ' + utc_time)
