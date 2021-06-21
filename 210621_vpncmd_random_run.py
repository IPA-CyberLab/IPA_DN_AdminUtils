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
import random
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
from datetime import timedelta, tzinfo, timezone, time, date, datetime

from submodules.IPA_DN_PyNeko.v1.PyNeko import *

def DoOnce():
    TIMEOUT_MAX_SECS = 90
    timeout = float(Rand.SInt31() % (TIMEOUT_MAX_SECS * 1000)) / 1000.0
    print()
    print("--------------")
    print(F"starting vpncmd. timeout={timeout}")
    print()
    EasyExec.Run(["/root/vpncmd/vpnclient/vpncmd", "/tools", "/cmd:ts"], timeoutSecs=timeout, shell=False)
    print("vpncmd finish ok.")

if __name__ == '__main__':

    while True:
        try:
            DoOnce()
            print(F"{Time.NowLocal()}: Finished.")
        except Exception as err:
            print(F"{Time.NowLocal()}: {err}.")

        Kernel.SleepRandInterval(15)
        







