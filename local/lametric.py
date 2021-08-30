from upnpclient import discover as _upnp_discover
from requests import Session
from base64 import b64encode as _b64encode


class Time:
    def __init__(self, key: str, IP: str, version: str = 'v2'):
        self.key = _b64encode(s=f'dev:{key}'.encode()).decode()
        self.url = f'http://{IP}:8080/api/{version}'
        self.headers = {'Authorization': 'Basic ' + self.key}
        self.s = Session()

    def notify(self, mood, text):
        r = self.s.post(
            self.url + "/device/notifications", 
            json={
                'priority': "critical",
                'icon_type': "info", # none, info, alert
                'lifeTime': 10 * 1000,
                'model': {
                    'frames': [
                        {'text': mood},
                        {'text': text},
                    ],
                    'sound': {'category': "notifications", 'id': "notification", 'repeat': 1},
                    'cycles': 1
                }
            },
            headers=self.headers
        )
        print(r.text)
        # print(r.ok)

def cacheIP(IP: str):
    with open("IP.txt", "w") as f:
        f.write(IP)

def getCachedIP() -> str:
    try:
        with open("IP.txt", "r") as f:
            return f.read()
    except:
        return False

def discover(key: str) -> Time:
    IP = getCachedIP()
    if not IP:
        print("[!] IP is not cached")
    else:
        print("[+] IP is cached")
        return Time(key, IP)
        
    print("[+] Searching for devices on your network...")
    for device in _upnp_discover():
        if device.manufacturer == 'LaMetric Inc.':
            if device.model_name == 'LaMetric Time':
                IP = device._url_base.replace(':443', '').replace('https://', '')
                cacheIP(str(IP))
                print("[+] Found laMetric Time! IP: " + IP)
                return Time(key, IP)
    print("[!] Couldn't find laMetric Time on your network")