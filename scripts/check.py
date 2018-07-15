#!/usr/bin/env python3

import contextlib
import json
import os
import sys

import apt

from common import make_single_repo_apt_cache

stdout_fd = sys.stdout.fileno()

with contextlib.redirect_stdout(sys.stderr):
    config = json.loads(sys.stdin.read())

    try:
        repo = config['source']['repository']
        package_name = config['source']['package']
    except KeyError as e:
        print('required parameter "' + e.args[0] + '" missing')
        exit(1)

    version = config['version']['id'] if config['version'] is not None else None

    cache = make_single_repo_apt_cache(repo)

    pkg = cache[package_name]
    pkg_versions = [version.version for version in pkg.versions][::-1]

    if not version or len(pkg_versions) == 0:
        new_versions = pkg_versions
    elif version not in pkg_versions:
        new_versions = pkg_versions[-1]
    else:
        index = pkg_versions.index(version)
        new_versions = pkg_versions[index:-1]

    os.write(
        stdout_fd,
        json.dumps(
            [
                {'id': version} for version in new_versions
            ]
        ).encode('utf-8')
    )
