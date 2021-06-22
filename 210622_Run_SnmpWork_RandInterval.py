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

def RunOnce():
    PrintLog("--- Starting the process... ---")
    p = EasyExec.RunBackground("/root/IPA-DN-Cores/Cores.NET/Dev.Test/bin/Release/net5.0/Dev.Test -debugmode ReleaseNoLogs -notelnet SnmpWorkDaemon test".split(),
                               shell=False, cwd="/root/IPA-DN-Cores/Cores.NET/Dev.Test/",
                               stdin=subprocess.PIPE)
    try:
        secs = Util.GenRandInterval(60.0)
        PrintLog(F"Sleeping for {secs} secs...")
        Kernel.Sleep(secs)

        PrintLog("Sending Enter key...")
        p.stdin.write("\n")
        p.stdin.flush()

        PrintLog("Waiting...")
        p.wait()

        PrintLog("Ok.")
    except:
        try:
            PrintLog("Killing the process...")
            p.kill()
            PrintLog("Kill OK.")
        except:
            PrintLog("Kill Error.")
            pass
        raise
    


if __name__ == '__main__':

    while True:
        try:
            RunOnce()
            PrintLog("Finished.")
        except Exception as err:
            PrintLog(err)

        Kernel.SleepRandInterval(1.0)
        







