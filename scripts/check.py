#!/usr/bin/env python3

import contextlib
import json
import os
import sys

import apt_repo
import packaging.version

stdout_fd = sys.stdout.fileno()

with contextlib.redirect_stdout(sys.stderr):
    config = json.loads(sys.stdin.read())

    try:
        repos = config['source']['repositories']
        package_name = config['source']['package']
    except KeyError as e:
        print('required parameter "' + e.args[0] + '" missing')
        exit(1)

    version = config['version']['id'] if 'version' in config and config['version'] is not None else None

    sources = apt_repo.APTSources(
        [apt_repo.APTRepository.from_sources_list_entry(repo) for repo in repos]
    )
    pkgs = sources[package_name]
    pkg_versions = [pkg.version for pkg in pkgs]
    pkg_versions.sort(key=lambda el: packaging.version.parse(el))

    if version not in pkg_versions:
        # Either:
        #   This is a fresh check (ie no 'current' version), so we return the latest version
        #   This version is no longer available from apt, so we return the latest version
        new_versions = pkg_versions[-1:]
    else:
        # Otherwise, we return everything newer than the current version, including the current version
        index = pkg_versions.index(version)
        new_versions = pkg_versions[index:]

    os.write(
        stdout_fd,
        json.dumps(
            [
                {'id': version} for version in new_versions
            ]
        ).encode('utf-8')
    )
