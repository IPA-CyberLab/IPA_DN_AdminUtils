#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021- IPA CyberLab.
# All Rights Reserved.
#
# Author: Daiyuu Nobori

import os
import json
import subprocess
import inspect
import typing
import time as systime
import argparse
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
from datetime import timedelta, tzinfo, timezone, time, date, datetime

from submodules.IPA_DN_PyNeko.v1.PyNeko import *



# メイン処理
if __name__ == '__main__':
    # 引数解析
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_fqdn", metavar="<Domain FQDN>",
                        type=str, help="Specify domain fqdn (e.g. abc.example.org)")
    parser.add_argument("master_server", metavar="<Primary Server IP>",
                        type=str, help="Specify IP address (e.g. 1.2.3.4)")

    args = parser.parse_args()
    domain_fqdn: str = args.domain_fqdn
    domain_fqdn = Str.Trim(domain_fqdn).lower()

    master_server: str = args.master_server
    master_server = Str.Trim(master_server).lower()

    includes_filepath = "/etc/bind/named.conf.local"

    zone_filepath = "/etc/bind/slaves/" + domain_fqdn + ".conf"

    body = Lfs.ReadAllText(includes_filepath)

    if not Str.InStr(body, f"/{domain_fqdn}.conf\""):
        body += f"include \"/etc/bind/slaves/{domain_fqdn}.conf\";\n"
        Lfs.WriteAllText(includes_filepath, body)
    
    body = Str.ReplaceMultiStr("""
zone "__FQDN__" IN {
  type slave;
  masters { __IP__; };
  file "__FQDN__.zone";
  check-names ignore;
};
""", {"__FQDN__": domain_fqdn, "__IP__": master_server})

    Lfs.WriteAllText(zone_filepath, body)







