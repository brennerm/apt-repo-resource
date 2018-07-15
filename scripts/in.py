#!/usr/bin/env python3

import contextlib
import json
import os
import sys
import urllib.request

import apt

from common import make_single_repo_apt_cache

stdout_fd = sys.stdout.fileno()

with contextlib.redirect_stdout(sys.stderr):
    dest = sys.argv[1]
    config = json.loads(sys.stdin.read())

    try:
        repo = config['source']['repository']
        package = config['source']['package']
    except KeyError as e:
        print('required parameter "' + e.args[0] + '" missing')
        exit(1)

    version = config['version']['id']

    with open(os.path.join(dest, 'package'), 'w') as f:
        f.write(config['source']['package'])

    with open(os.path.join(dest, 'version'), 'w') as f:
        f.write(version)

    if config['params']['download_deb']:
        cache = apt.Cache()
        url = cache[package].versions[version].uri
        filename = url.split('/')[-1]

        urllib.request.urlretrieve(
            url,
            os.path.join(dest, filename)
        )

        with open(os.path.join(dest, 'filename'), 'w') as f:
            f.write(filename)

    os.write(
        stdout_fd,
        json.dumps(
            {
                'version': config['version'],
                'metadata': []
            }
        ).encode('utf-8')
    )
