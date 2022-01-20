# -*- coding: utf-8 -*-

import qbittorrentapi
import transmission_rpc

from typing_extensions import Literal
from attrdict import AttrDict


class Client:
    type = None
    client = None

    _qbt = 'qBittorrent'
    _transmission = 'transmission'

    def __init__(
            self,
            user: str,
            password: str,
            client: Literal[None, 'qBittorrent', 'transmission'] = _qbt,
            host: str = 'http://localhost',
            port: int = 8080,
            **kwargs
    ):
        self.type = client or self._qbt

        if self.type == self._qbt:
            self.client = qbittorrentapi.Client(
                host=host,
                username=user,
                password=password,
                port=port)
            print(f'{self.type}: {self.client.server_version()}')
        elif self.type == self._transmission:
            self.client = transmission_rpc.Client(
                username=user,
                password=password,
                port=port,
                host=host, )
            print(f'{self.type}: {self.client.server_version}')
        else:
            raise 'client.type должен быть qBittorrent или transmission'

    def torrent_comments(self):
        res = []
        if self.type == self._qbt:
            for t in self.client.torrents_info():
                d = AttrDict({'hash': t['hash'],
                              'comment': self.client.torrents_properties(torrent_hash=t['hash']).get('comment'),
                              'name': t['name']})
                res.append(d)
        elif self.type == self._transmission:
            for t in self.client.get_torrents():
                comment = t.comment
                d = AttrDict({'hash': t.hashString,
                              'comment': comment,
                              'name': t.name})
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
