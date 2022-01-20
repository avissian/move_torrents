#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from yaml import full_load
import lib.client as c
import re

config = full_load(open('config.yml', 'r'))


def main():
    client = c.Client(**config.get('client'))

    skipped = 0

    for torrent_comments in client.torrent_comments():
        gr = re.match(config['do']['regexp'], torrent_comments.comment)
        if gr:
            location = config['do']['new_path'] + '/' + gr.groups()[0]
            print(f'move "{torrent_comments.name}" to {location}')
            client.move(torrent_hash=torrent_comments.hash, location=location)
        else:
            print(f'skip "{torrent_comments.name}" comment: {torrent_comments.comment}')
            skipped += 1

    if skipped > 0:
        print(f'\nSkipped: {skipped}')


if __name__ == '__main__':
    main()
