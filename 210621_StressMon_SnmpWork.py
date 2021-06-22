﻿#!/usr/bin/env python3
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
import random
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
from datetime import timedelta, tzinfo, timezone, time, date, datetime

from submodules.IPA_DN_PyNeko.v1.PyNeko import *

def ReportOnce():
    http = HttpClient()
    res = http.Get("http://127.0.0.1:7007/?method=getall")

    c = StressMonClient()
    c.Report(res.Body)


if __name__ == '__main__':

    while True:
        try:
            ReportOnce()
            print(F"{Time.NowLocal()}: Reported.")
        except Exception as err:
            print(F"{Time.NowLocal()}: {err}.")

        Kernel.SleepRandInterval(10.0)
        







