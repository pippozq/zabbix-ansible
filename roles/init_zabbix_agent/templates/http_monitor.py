#!/usr/bin/env python
import sys
import httplib

if __name__ == '__main__':

    addr = '{{ansible_hostname}}'
    port = int(sys.argv[1])
    check_url = '/'
    r1 = None
    try:
        conn = httplib.HTTPConnection(addr, port, timeout=20)
        conn.request("GET", check_url)
        r1 = conn.getresponse()
    except Exception,e:
        print e
    if r1 is not None:
        print r1.status

