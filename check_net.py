#!/usr/bin/env python3
"""Five-second egress check: can this host actually reach the job boards?

Run this FIRST after changing an environment's network policy — it tells you in
seconds whether `python run.py --days 5` will collect anything, instead of
finding out after a full crawl.

    python check_net.py
"""
import sys

import requests

import sources as S

PROBES = ["https://th.jobsdb.com/robots.txt", "https://www.jobthai.com/robots.txt",
          "https://th.indeed.com/robots.txt", "https://www.linkedin.com/robots.txt",
          "https://www.jobth.com/robots.txt", "https://www.google.com/robots.txt"]

ok = 0
for url in PROBES:
    try:
        code = requests.get(url, headers=S.HEADERS, timeout=15).status_code
        ok += code == 200
        print(f"  {code}  {url}")
    except requests.RequestException as exc:
        note = ("BLOCKED by egress proxy" if "ProxyError" in type(exc).__name__ or
                "Tunnel" in str(exc) else type(exc).__name__)
        print(f"  ---  {url}   <- {note}")

print(f"\n{ok}/{len(PROBES)} reachable — "
      + ("egress is open, run: python run.py --days 5" if ok else
         "still blocked; the pipeline will report every source as BLOCKED"))
sys.exit(0 if ok else 1)
