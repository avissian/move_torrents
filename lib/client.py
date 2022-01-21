# -*- coding: utf-8 -*-
import logging

from qbittorrentapi import Client as Qbt
from transmission_rpc import Client as Transmission

from typing_extensions import Literal
from collections import namedtuple


class Client:
    type = None

    client = None

    _qbt = 'qBittorrent'
    _transmission = 'transmission'

    t_comment = namedtuple('comments', ['hash', 'comment', 'name'])

    def __init__(self,
                 user: str,
                 password: str,
                 client: Literal[None, 'qBittorrent', 'transmission'] = _qbt,
                 host: str = 'http://localhost',
                 port: int = 8080,
                 **kwargs):
        self.type = client or self._qbt

        if self.type == self._qbt:
            self.client = Qbt(host=host,
                              username=user,
                              password=password,
                              port=port)
            logging.debug(f'{self.type}: {self.client.app_version()}')
        elif self.type == self._transmission:
            self.client = Transmission(username=user,
                                       password=password,
                                       port=port,
                                       host=host, )
            logging.debug(f'{self.type}: {self.client.server_version}')
        else:
            raise 'client.type должен быть qBittorrent или transmission'

    def torrent_comments(self):
        res = []
        if self.type == self._qbt:
            for t in self.client.torrents_info():
                d = self.t_comment(hash=t['hash'],
                                   comment=self.client.torrents_properties(torrent_hash=t['hash']).get('comment'),
                                   name=t['name'])
                res.append(d)
        elif self.type == self._transmission:
            for t in self.client.get_torrents():
                d = self.t_comment(hash=t.hashString, comment=t.comment, name=t.name)
                res.append(d)

        return res

    def move(self, torrent_hash, location):
        if self.type == self._qbt:
            self.client.torrents_set_location(
                location=location,
                torrent_hashes=torrent_hash
            )
        elif self.type == self._transmission:
            self.client.move_torrent_data(
                ids=torrent_hash,
                location=location
            )
