#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import re
import time

from yaml import full_load

import lib.client as c

config = full_load(open('config.yml', 'r'))


def main():
    client = c.Client(**config.get('client'))

    skipped = 0

    for torrent_comments in client.torrent_comments():
        gr = re.match(config['do']['regexp'], torrent_comments.comment)
        if gr:
            location = os.path.join(config['do']['new_path'], gr.groups()[0])
            logging.info(f'move "{torrent_comments.name}" to {location}')
            if config['do'].get('test_run', False):
                logging.debug('simulate')
            else:
                client.move(torrent_hash=torrent_comments.hash, location=location)
        else:
            logging.info(f'skip "{torrent_comments.name}" comment: {torrent_comments.comment}')
            skipped += 1

    if skipped > 0:
        logging.info(f'\nSkipped: {skipped}')


if __name__ == '__main__':
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    try:
        os.mkdir("./logs")
    except FileExistsError:
        pass

    handler = logging.StreamHandler()
    formatter = logging.Formatter(u"[%(asctime)s.%(msecs)03d] %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    f_handler = logging.FileHandler("./logs/" + time.strftime("%y%m%d.log"), encoding="utf-8")
    f_formatter = logging.Formatter(u"%(filename)-.10s[Ln:%(lineno)-3d]%(levelname)-8s[%(asctime)s]|%(message)s")
    f_handler.setFormatter(f_formatter)
    f_handler.setLevel(logging.NOTSET)
    logger.addHandler(f_handler)

    """ *** """

    main()
