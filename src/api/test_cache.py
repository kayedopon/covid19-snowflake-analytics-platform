import time

import requests


URL = "http://127.0.0.1:8000/covid/top/deaths/2022"


def make_request():
    start = time.perf_counter()
    response = requests.get(URL)
    elapsed = time.perf_counter() - start

    print(f"Status: {response.status_code}")
    print(f"Cache: {response.headers.get('X-Cache')}")
    print(f"Time: {elapsed * 1000:.2f} ms")
    print()


make_request()
make_request()