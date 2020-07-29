import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

def get_proxie(ip):
    proxie={
        'http':'http://'+ip
    }
    return proxie

ips=[]
while(len(ips)<5):
    http=get_proxie(get_proxy())
    if not http in ips:
        ips.append(http)
print(ips)