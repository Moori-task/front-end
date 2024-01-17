import httpx
import requests

proxies = {
  'http': 'http://192.168.43.1:18009',
  'https': '192.168.43.1:18009',
}

with httpx.Client(proxies='socks5://192.168.43.1:18008') as client:
  jj = client.get(url="https://api.telegram.org/bot6484830100:AAG9itC_ZgVbLvmAVvK6oVb3HLi8tC4DRlE/getUpdates")
print(jj)