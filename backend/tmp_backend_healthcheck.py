import urllib.request
urls = [
    'http://127.0.0.1:8000/candidates?limit=1&offset=0',
    'http://127.0.0.1:8000/sessions?limit=1&offset=0',
]
for url in urls:
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            print(url, resp.status)
            print(resp.read().decode())
    except Exception as exc:
        print(url, 'ERROR', exc)
