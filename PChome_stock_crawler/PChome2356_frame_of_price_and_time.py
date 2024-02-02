import requests
import re
import pandas as pd



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}
data = {
    'is_check': 1
}
code = '2356'
res = requests.post(f'https://pchome.megatime.com.tw/stock/sto0/ock3/sid{code}.html', headers=headers, data=data).text


columns = re.findall('<td height=\d+ class=t12>(.*?)</td>', res)
res = re.sub(r'<font color=#......>|</font>', '', res)
price_vol_list = re.findall('<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(\d+)</td></tr>', res)
data_to_df = dict(zip(columns, list(zip(*price_vol_list))))
price_vol_df = pd.DataFrame(data_to_df)
price_vol_df.to_csv(f'PCHome_stock_{code}.csv')