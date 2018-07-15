#!/usr/bin/env python3

import tempfile

import apt


def make_single_repo_apt_cache(repo):
    cache = apt.Cache(memonly=True)

    with tempfile.NamedTemporaryFile('w') as tmp_file:
        tmp_file.file.write(repo)
        cache.update(sources_list=tmp_file.name)

    cache.open()
    return cache
