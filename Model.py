import cx_Oracle

class Model:

    def __init__(self):
        self.song_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = cx_Oracle.connect("music_player/music@127.0.0.1")
            self.cur = self.conn.cursor()

        except cx_Oracle.DatabaseError as ex:
            print("Db Error", ex)
            self.db_status = False

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

    def add_song(self, song_name, song_path):
        self.song_dict[song_name] = song_path

    def get_song_path(self, song_name):
        return self.song_dict[song_name]

    def remove_song(self, song_name):
        self.song_dict.pop(song_name)

    def search_song_in_favourites(self, song_name):
        self.cur.execute("select SONG_NAME from myfavourite where SONG_NAME=:1", (song_name,))
        song_tuple = self.cur.fetchone()
        if song_tuple is None:
            return False
        else:
            return True

    def add_song_to_favourites(self, song_name):
        try:
            is_song_present = self.search_song_in_favourites(song_name)
            if is_song_present is True:
                return "Selected Song Already Present in Favourites"
            else:
                song_path = self.song_dict[song_name]
                self.cur.execute("select max(SONG_ID) from myfavourite")
                prev_song_id = self.cur.fetchone()[0]
                if prev_song_id is None:
                    prev_song_id = 0
                next_song_id = prev_song_id + 1
                self.cur.execute("insert into myfavourite values(:1,:2,:3)", (next_song_id, song_name, song_path))
                self.conn.commit()
                return "Song Added To Favourites"
        except cx_Oracle.DatabaseError:
            return "DataBase Error, Unable to Add To Favourite"

    def load_song_from_favourite(self):
        try:
            self.cur.execute("select SONG_NAME,SONG_PATH from myfavourite")
            song_present = False
            for song_name, song_path in self.cur:
                self.song_dict[song_name] = song_path
                song_present = True
            if song_present is True:
                return "List Populated From Favourite", self.song_dict
            else:
                return "Favourite list empty",
        except cx_Oracle.DatabaseError:
            return "Unable To Reach Database, Try Again !!!",

    def remove_song_from_favourite(self, song_name):
        try:
            is_song_present = self.search_song_in_favourites(song_name)
            if is_song_present is True:
                self.cur.execute("delete from myfavourite where SONG_NAME=:1", (song_name,))
                self.conn.commit()
                return "Song Removed From Favourites"
            else:
                return "Selected Song Not Present In Favourites "
        except cx_Oracle.DatabaseError:
            return "DataBase Error, Unable to Remove From Favourite"


obj = Model()
