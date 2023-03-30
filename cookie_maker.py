from http import cookies
import datetime
import requests

def show_cookie():
    print(requests.get("http://localhost:8001"))
    #for key, morsel in c.items():
        #print()
        #print('key =', morsel.key)
        #print('  value =', morsel.value)
        #print('  coded_value =', morsel.coded_value)
        #return morsel

def make_cookie():
    cookies = {'auth': 'yes'}
    r = requests.post('http://localhost:8001', cookies=cookies)