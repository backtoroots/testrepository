import requests
import json
import time
import datetime as dt


def connect():
    payload = {'limit':'10', 'sort':'volume_24h', 'sort_dir':'desc'}
    headers = {'X-CMC_PRO_API_KEY':'fdc5337f-9775-40a2-a211-f34b15f4521e'}
    response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
                        params=payload, headers=headers, stream=True)
    check(response)


def check(response):
    print(response.text)
    print('size in kb', len(response.content)/1024)
    decode = json.loads(response.text)
    print(response.elapsed.total_seconds())
    actualTime = 1
    for i in range(10):
        firstTime = decode['data'][i]['last_updated']
        firstTime = time.strptime(firstTime[:10] + ' ' + firstTime[11:-5], "%Y-%m-%d %H:%M:%S")
        end = dt.datetime(firstTime[0], firstTime[1], firstTime[2], firstTime[3], firstTime[4], firstTime[5])
        n = dt.datetime.now()
        x = n - end
        if x.days > 0:
            actualTime = 0
            break
        print(actualTime)
    if ((len(response.content)/1024) < 10) and (response.elapsed.total_seconds() < 0.00500) and (actualTime == 1):
        print('Test finished successfully')
    else:
        print('Test failed')


connect()

