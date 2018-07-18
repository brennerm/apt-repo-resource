#!/usr/bin/env python3

import contextlib
import json
import os
import sys
import urllib.request

import apt_repo

stdout_fd = sys.stdout.fileno()

with contextlib.redirect_stdout(sys.stderr):
    dest = sys.argv[1]
    config = json.loads(sys.stdin.read())

    try:
        repos = config['source']['repositories']
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
        sources = apt_repo.APTSources(
            [apt_repo.APTRepository.from_sources_list_entry(repo) for repo in repos]
        )
        url = sources.get_package_url(package, version)
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
