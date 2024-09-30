import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 "
                  "Safari/537.36"
}


def Net_Get(url):
    try:
        rp = requests.get(url, headers=headers)
    except Exception as e:
        rp = None
        print(e)
    return rp.text
