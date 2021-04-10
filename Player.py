from pygame import mixer
from tkinter import filedialog
import os
import Model
from mutagen.mp3 import MP3


class Player:

    def __init__(self):
        mixer.init()
        self.my_model = Model.Model()
        self.song_path = None
        self.audio_file = None

    def get_db_status(self):
        return self.my_model.get_db_status()

    @staticmethod
    def set_volume(volume_level):
        mixer.music.set_volume(volume_level)

    def add_song(self):
        song_paths = filedialog.askopenfilename(title="Song Selection", filetype=[("Mp3 file", "*.mp3")], multiple=True)
        song_name = []
        for single_song_path in song_paths:
            song = os.path.basename(single_song_path)
            present_in_dict = song in self.my_model.song_dict
            song_name.append([song, present_in_dict])
            self.my_model.add_song(song, single_song_path)
        return song_name

    def remove_song(self, song_name):
        self.my_model.remove_song(song_name)

    def get_song_length(self, song_name):
        self.song_path = self.my_model.get_song_path(song_name)
        self.audio_file = MP3(self.song_path)
        song_length = self.audio_file.info.length
        return song_length

    def play_song(self):
        mixer.quit()
        mixer.init(frequency=self.audio_file.info.sample_rate)
        mixer.music.load(self.song_path)
        mixer.music.play()

    @staticmethod
    def stop_song():
        mixer.music.stop()

    @staticmethod
    def pause_song():
        mixer.music.pause()

    @staticmethod
    def unpause_song():
        mixer.music.unpause()

    def add_song_to_favourites(self, song_name):
        result = self.my_model.add_song_to_favourites(song_name)
        return result

    def load_song_from_favourites(self):
        result = self.my_model.load_song_from_favourite()
        return result

    def remove_song_from_favourites(self, song_name):
        result = self.my_model.remove_song_from_favourite(song_name)
        return result

    def close_player(self):
        mixer.music.stop()
        self.my_model.close_db_connection()
