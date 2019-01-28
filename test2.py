import requests
import json
import time
import datetime as dt
from queue import Queue
from threading import Thread


def connect(all_time_q, flag_q):
    payload = {'limit':'10', 'sort':'volume_24h', 'sort_dir':'desc'}
    headers = {'X-CMC_PRO_API_KEY':'fdc5337f-9775-40a2-a211-f34b15f4521e'}
    response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
                        params=payload, headers=headers, stream=True)
    check(response, all_time_q, flag_q)


def check(response, all_time_q, flag_q):
    print('size in kb', len(response.content)/1024)
    decode = json.loads(response.text)
    all_time_q.put(response.elapsed.total_seconds())
    print(response.elapsed.total_seconds())
    actual_time = 1
    for i in range(10):
        first_time = decode['data'][i]['last_updated']
        first_time = time.strptime(first_time[:10] + ' ' + first_time[11:-5], "%Y-%m-%d %H:%M:%S")
        end = dt.datetime(first_time[0], first_time[1], first_time[2], first_time[3], first_time[4], first_time[5])
        n = dt.datetime.now()
        x = n - end
        if x.days > 0:
            actual_time = 0
            break
    if ((len(response.content)/1024) > 10) or (response.elapsed.total_seconds() >= 0.00500) or (actual_time == 0):
        flag_q.put(1)
    else:
        flag_q.put(0)


all_time = 0
flag = 0
all_time_q = Queue()
flag_q = Queue()
thread = []
for i in range(8):
    thread.append(Thread(target=connect, args=(all_time_q, flag_q)))
    thread[i].start()
    thread[i].join()

for i in range(8):
    flag = (flag or flag_q.get())
    all_time += all_time_q.get()
print('\ntime is ', all_time)
rps = 8/all_time
print('rps is ', rps)
if (rps > 5) and (flag == 0) and (all_time*0.1 < 0.00450):
    print('\nTest finished successfully')
else:
    print('Test failed')
