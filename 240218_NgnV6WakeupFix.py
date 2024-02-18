#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024- IPA CyberLab.
# All Rights Reserved.
#
# Author: Daiyuu Nobori

# 目的:
# ある地域電話会社の NGN を、単なる一ユーザーとして利用していて、IPv6 ネイティブ通信を楽しんでいるが、
# 収容ルータのうち、A 社製のルータで、稀に IPv6 スタックにバグが生じるようである。
# 
# 某独立行政法人で契約している 1 本の FTTH 回線で、このバグに悩まされている。
# 日本全国で同じ型の NGN の FTTH 回線を何本も契約しているが、他では発生していないので、
# おそらく、この A 社製の収容ルータのソフトウェアかハードウェアの、大変深いバグが一度
# 発動した (これは、とても低い確率で発生するのであろう) のちに、ずっとそのままその 1 台の
# 筐体のみがバグを生じさせているのであろう。
# 
# バグの概要:
# 収容ルータのコントロールプレーンにおける IPv6 ND の応答パケットがうまく
# 収容ルータのデータプレーンにおけるハードウェア上の ND キャッシュに反映されない。
# 無通信状態が一定時間継続すると、それ以降、IPv6 通信ができなくなる。
# 
# 対処法:
# なぜか、収容ルータから割り当てられる自機の IPv6 Prefix (/64) に ::fffe を付加したもの
# に対して ping を打つと、たちどころに、問題が解決できる。
# 
# そこで、これを自動化するスクリプトを、作成したのである。

import os
import json
import subprocess
import inspect
import typing
import time as systime
import argparse
import random
import ipaddress
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
from datetime import timedelta, tzinfo, timezone, time, date, datetime

from submodules.IPA_DN_PyNeko.v1.PyNeko import *

def ReportOnce():
    tmp = "Hello! Now: " + Time.ToYYYYMMDDHHMMSS(Time.NowLocal())

    c = StressMonClient()
    c.Report(tmp)

def PerformOnce():
    # まず、自機に割り当てられている IPv6 アドレス一覧を列挙いたします。
    # 私は、プログラミングの素人ですので、ソケット API など使わず、ip コマンドを呼び出して結果を文字列パースするのです。
    # ip コマンドの --json オプションは、古い Linux では実装されていないので、使用してはいけません。
    # 文字列を頑張ってパースしましょう。
    res = EasyExec.RunPiped(
        F"/usr/sbin/ip -6 a".split(),
        shell=False,
        timeoutSecs=15)

    # 超手抜きパーサー
    lines = Str.GetLines(res.StdOut, removeEmpty=True, trim=True)

    # ターゲットの IPv4 アドレス一覧の生成
    targetList: List[str] = list()

    for line in lines:
        try:
            tokens = line.split()
            if len(tokens) >= 4 and tokens[0] == "inet6" and tokens[2] == "scope" and tokens[3] == "global":
                ipnetwork:ipaddress.IPv6Network = ipaddress.ip_network(tokens[1], strict=False)
                if ipnetwork.prefixlen == 64:
                    prefix = ipnetwork.network_address
                    fffe_address = prefix + 0xfffe
                    targetList.append(Str.ToStr(fffe_address))
        except:
            DoNothing()
    
    # ping を順番に打つ
    for target in targetList:
        try:
            EasyExec.RunPiped(
                F"/usr/bin/ping6 -c 5 -W 1 {target}".split(),
                shell=False,
                timeoutSecs=15)
        except:
            DoNothing()




if __name__ == '__main__':

    #PerformOnce()
    #exit()

    while True:
        try:
            PerformOnce()
        except Exception as err:
            DoNothing()

        Kernel.SleepRandInterval(30.0)
        







