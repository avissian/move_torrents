from yaml import full_load
import qbittorrentapi
import re

config = full_load(open('config.yml', 'r'))
client = None


def main():
    global client
    skipped = 0
    client_cfg = config.get('client')
    client = qbittorrentapi.Client(
        host=client_cfg.get('host', 'http://localhost:8080'),
        username=client_cfg.get('login', 'admin'),
        password=client_cfg.get('passw', 'adminadmin'))

    for torrent in client.torrents.info.all():
        comment = client.torrents_properties(torrent_hash=torrent['hash'])['comment']
        gr = re.match(config['do']['regexp'], comment)
        if gr:
            location = config['do']['new_path'] + '/' + gr.groups()[0]
            print(f'move {torrent["name"]} to {location}')
            client.torrents_set_location(
                location=location,
                torrent_hashes=torrent['hash']
            )
        else:
            print(f'skip {torrent["name"]}')
            skipped += 1

    if skipped > 0:
        print(f'\nSkipped: {skipped}')


if __name__ == '__main__':
    main()
