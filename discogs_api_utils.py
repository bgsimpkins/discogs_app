import discogs_client
from discogs_data_classes import RecordMaster
from datetime import datetime


class DiscogsQueryer:

    def __init__(
        self,
        token: str
    ):
        self.token = token
        self.d = discogs_client.Client('my_user_agent/1.0', user_token=token)

    def search_by_artist(self, album_name):
        return self.d.search(album_name, type='master')

    def search_by_artist_and_album(self, artist_name: str, album_name: str, max_recs: int):
        artist_name = artist_name.strip()
        album_name = album_name.strip()

        albums = self.d.search(album_name, artist=artist_name, type='master')
        print('{num_albums} albums found with name {album_name}. Going with first one...'.format(
            num_albums=len(albums),
            album_name=album_name
        ))
        num_searched = 0
        res_list = []
        for a in albums:

            #data = json.loads(a.data)
            print(a.data)
            mr = a.main_release

            # TODO: Assumption here is that first return is most relevant/available. Might need to test this.
            if mr is not None: #and mr.artists[0].name.lower() == artist_name.lower():
                print('Found: artist={} master={}'.format(mr.artists[0].name, a))

                res_list.append(
                    RecordMaster(
                        master_id=a.data['master_id'],
                        master_url=a.url,
                        artist=mr.artists[0].name,
                        title=a.data['title'],
                        formats=', '.join(a.data['format']),
                        year=a.data['year'],
                        country=a.data['country'],
                        date_created=None,
                        date_updated=None
                    )
                )

            num_searched += 1
            if num_searched > max_recs:
                print('Max number of records searched ({}). Please refine your search'.format(max_recs))
                break
        return res_list

    def get_master(self, id):
        a = self.d.master(id)
        if a is not None:
            mr = a.main_release
            return RecordMaster(
                        master_id=a.data['id'],
                        master_url=a.data['uri'],
                        artist=mr.artists[0].name,
                        title=mr.title,
                        formats=None,
                        year=mr.year,
                        country=mr.country,
                        date_created=datetime.now(),
                        date_updated=None
                    )
        else:
            print('Couldn''t find master {id}!')
            return None
