import discogs_client
import re
import datetime

import pandas as pd
from dotenv import load_dotenv
import emailUtils
import requests

import dbUtils
from dbUtils import *
from discogs_api_utils import DiscogsQueryer
from discogs_data_classes import RecordMaster

def test_ping_python_api():

    user_token = 'ESnFpwcSRnXTfmetrhmFHUUqGFmceYxacfmzglHG'
    d = discogs_client.Client('my_user_agent/1.0', user_token=user_token)
    res = d.search('Sunburst Finish', type='release')
    for r in res:
        print(r)

def test_ping():
    user_token = 'ESnFpwcSRnXTfmetrhmFHUUqGFmceYxacfmzglHG'
    params={'user-agent':'my_user_agent/1.0','token': user_token, 'q': 'Rush'}

    #r = requests.get('https://api.discogs.com/database/search', params=params)
    r = requests.get('https://api.discogs.com/releases/249504')
    print('status code={}'.format(r.status_code))
    print(r)

def test_thing():
    load_dotenv()

    # user_token = 'dxAClTChBwQmogBJASJpcnfelueWbSwcDeDoeQje'
    # conn = dbUtils.connect_to_db()
    # dbUtils.set_token(conn, user_token)
    # token_row = dbUtils.get_current_token(conn)
    # print('token={}'.format(token_row['token']))
    # print('token_date={}'.format(token_row['token_date']))

    ##Get row as series from DataFrame
    # d = {'col1': [1, 2], 'col2': [3, 4]}
    # df = pd.DataFrame(data=d)
    # row1 = df.iloc[0]
    # print(row1)

    # d = {'token': 'abc', 'date': datetime.time}
    # s = pd.Series(d, copy=False)
    # print(s)

    # dollar_patt = '\$\d+(?:\.\d+)?'
    # p = re.compile(dollar_patt)
    # print(p.findall('about $20.44 total'))

    ##############
    #dq = DiscogsQueryer('IHIkOJLvpFtBReTeRCDmvdlzIJGxJSSgffjdKbXc')

    # album = dq.search_by_artist_and_album('Rush','Signals')
    # print(album)

    # master: RecordMaster = dq.get_master(12703)
    # print(master)
    # print(master.__dict__)

    ##############
    # conn = dbUtils.connect_to_db()
    # wl = dbUtils.get_watchlist(conn)
    # print(wl)
    conn = dbUtils.connect_to_db()
    wl_item = dbUtils.get_watchlist_item(conn, 35137)
    print(wl_item)

def test_email():
    emailUtils.test()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #test_email()
    test_ping()
    #test_ping_python_api()
    #test_thing()

