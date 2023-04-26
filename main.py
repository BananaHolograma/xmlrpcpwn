#!/usr/bin/env python -f
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_xmlrpc_is_open(url: str):
    http = urllib3.PoolManager(num_pools=2)

    base_url: str = url if url.endswith("/xmlrpc.php") else f"{url}/xmlrpc.php"
    print(f"[+] Checking url {base_url} is open via GET request...")

    response = http.request('GET', base_url)

    if response.status == 4105 and response.data == b'XML-RPC server accepts POST requests only.':
        return True
    else:
        print(
            f"[+] GET request dit not response data expected, trying alternative with POST request")

        body = """<?xml version="1.0" encoding="utf-8"?> 
    <methodCall> 
    <methodName>demo.sayHello</methodName> 
    <params></params> 
    </methodCall>"""
        response = http.request('POST', base_url, body=body, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            "Accept": 'application/xml, text/xml',
            "User-Agent": "curl/7.88.1"})
        print(base_url, response.status)
        return response.status in [200, 201] and re.search('hello!', str(response.data.decode('utf-8')),  re.IGNORECASE)


if __name__ == '__main__':
    if check_xmlrpc_is_open("https://example.com/xmlrpc.php"):
        print('xmlrpc is open')
    else:
        print("xmlrpc not vulnerable")
