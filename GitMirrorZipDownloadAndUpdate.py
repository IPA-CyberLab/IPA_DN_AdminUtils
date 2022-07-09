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


# メモ
# python3 C:\git\IPA_DN_AdminUtils\GitMirrorZipDownloadAndUpdate.py https://abc:def@dnt-gitlab-mirror1-static.sehosts.com/d/dnobori.pc_ahosan/auth/ c:\tmp\a1 c:\tmp\a2

# メイン処理
if __name__ == '__main__':
    # 引数解析
    parser = argparse.ArgumentParser()
    parser.add_argument("git_mirror_url", metavar="<git_mirror_url>",
                        type=str, help="Specify mirror URL (e.g. https://abc:def@dnt-gitlab-mirror1.sehosts.com/d/dnobori.pc_ahosan/auth/)")
    parser.add_argument("dest_dir", metavar="<dest_dir>",
                        type=str, help="Specify destination URL (e.g. /data1/abc/)")
    parser.add_argument("tmp_dir", metavar="<tmp_dir>",
                        type=str, help="Specify tmp dir (e.g. /tmp/abc/)")

    args = parser.parse_args()

    git_mirror_url: str = args.git_mirror_url

    tmp_dir: str = args.tmp_dir

    dest_dir: str = args.dest_dir

    if not dest_dir.endswith("/"):
        dest_dir = dest_dir + "/"

    Lfs.DeleteDirectoryRecursively(tmp_dir)

    Lfs.CreateDirectory(tmp_dir)

    zip_src_dir = tmp_dir + "/zip_src/"

    Lfs.CreateDirectory(zip_src_dir)

    zip_dst_dir = tmp_dir + "/zip_dst/"

    Lfs.CreateDirectory(zip_dst_dir)

    zip_filepath = zip_src_dir + "/zip.zip"

    remote_commit_filepath = zip_src_dir + "/commit_id.txt"

    EasyExec.Run(["curl", "--get", "--globoff", "--fail", "-k", "--verbose", "--pinnedpubkey", "sha256//S1UUg1nPQpRdJV3LHM7AKVUVffnABhWFBNbEBQyM6Cc=", git_mirror_url + "/_git_current_commit_id.txt", "-o", remote_commit_filepath])

    remote_commit_id = Str.GetLines(Lfs.ReadAllText(remote_commit_filepath))[0]

    local_commit_filepath = dest_dir + "/_git_current_commit_id.txt"

    try:
        local_commit_id = Str.GetLines(Lfs.ReadAllText(local_commit_filepath))[0]
    except:
        local_commit_id = "none"
    
    if not Str.IsSamei(local_commit_id, remote_commit_id):
        EasyExec.Run(["curl", "--get", "--globoff", "--fail", "-k", "--verbose", "--pinnedpubkey", "sha256//S1UUg1nPQpRdJV3LHM7AKVUVffnABhWFBNbEBQyM6Cc=", git_mirror_url + "/_download_zip/", "-o", zip_filepath])

        EasyExec.Run(["unzip", "-o", zip_filepath, "-d", zip_dst_dir])

        Lfs.CreateDirectory(dest_dir)

        #EasyExec.Run(["rsync", "-avc", "--delete-after", "--ignore-errors", zip_dst_dir, dest_dir])
        EasyExec.Run(["rsync", "-avc", "--delete-after", "--ignore-errors", "/cygdrive/c/TMP/a2/zip_dst/", "/cygdrive/c/TMP/a1/"])










