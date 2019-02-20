import requests
# запрос на сайт playOW и получение html кода
user_id = 'BANNANN-21961'

url = 'https://playoverwatch.com/en-gb/career/pc/' + user_id
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
r = requests.get(url, headers=headers)
# получение списка героев из сорев режима
heroes_list = str(r.text)
