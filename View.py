
import random
import threading
import sys
import tkinter as tk
import tkinter.ttk as ttk
import musicplayer_support
import platform
from tkinter import messagebox
import Player
from My_Exception import *
from pygame import mixer
import time



def vp_start_gui():
    # Starting point when module is the main routine.
    global root
    root = tk.Tk()
    icon = tk.PhotoImage(file="./icons/icon.png")
    root.iconphoto(root, icon)
    top = View(root)
    musicplayer_support.init(root, top)
    root.mainloop()



class View:

    def __init__(self, top=None):

        # This class configures and populates the top level window.
        # top is the top level containing window.
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font11 = "-family {Segoe UI} -size 11 -weight "  \
            "normal -slant roman -underline 0 -overstrike 0"
        font12 = "-family {Avenir Next Cyr} -size 9 -weight normal "  \
            "-slant roman -underline 0 -overstrike 0"
        font13 = "-family {Comic Sans MS} -size 14 -weight bold " \
                 "-slant italic -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win64":
            self.style.theme_use('winnative')
        self.style.configure('.', background="#616161")
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        top.geometry("800x550+368+157")
        top.title(" Mouzikka : Rhythm Of Your Heart ")
        top.configure(background="#fff")
        self.top = top
        self.check = False
        self.played = None
        self.length = None
        self.thread = None
        self.thread_running = False
        self.player = Player.Player()

        self.vinylRecordImage = tk.Label(top)
        self.vinylRecordImage.place(relx=0.0, rely=0.0, height=310, width=380)
        self.vinylRecordImage.configure(background="white")
        self.vinylRecordImage.configure(disabledforeground="#a3a3a3")
        self.vinylRecordImage.configure(foreground="#000000")
        self._img4 = tk.PhotoImage(file="./icons/vinylrecord.png")
        self.vinylRecordImage.configure(image=self._img4)
        self.vinylRecordImage.configure(text='''Label''')

        self.songName = tk.Label(top)
        self.songName.place(relx=0.440, rely=0.050, height=44, width=325)
        self.songName.configure(background="#fff")
        self.songName.configure(disabledforeground="#a3a3a3")
        self.songName.configure(font=font13)
        self.songName.configure(foreground="#000000")
        self.songName.configure(text="MOUZIKKA  ", fg="#616161")

        self.songProgress = ttk.Progressbar(top)
        self.songProgress.place(relx=0.393, rely=0.209, relwidth=0.495, relheight=0.0, height=7)

        self.songTotalDuration = ttk.Label(top)
        self.songTotalDuration.place(relx=0.845, rely=0.165, height=19, width=41)
        self.songTotalDuration.configure(background="#fff")
        self.songTotalDuration.configure(foreground="#3399ff")
        self.songTotalDuration.configure(font=font12)
        self.songTotalDuration.configure(relief='flat', text="00:00")

        self.songTimePassed = ttk.Label(top)
        self.songTimePassed.place(relx=0.393, rely=0.165, height=19, width=41)
        self.songTimePassed.configure(background="#fff")
        self.songTimePassed.configure(foreground="#3399ff")
        self.songTimePassed.configure(font=font12)
        self.songTimePassed.configure(relief='flat', text="00:00")

        self.pauseButton = tk.Button(top)
        self.pauseButton.place(relx=0.580, rely=0.270, height=38, width=38)
        self.pauseButton.configure(activebackground="#ececec")
        self.pauseButton.configure(activeforeground="#000000")
        self.pauseButton.configure(background="#fff")
        self.pauseButton.configure(borderwidth="0")
        self.pauseButton.configure(disabledforeground="#a3a3a3")
        self.pauseButton.configure(foreground="#000000")
        self.pauseButton.configure(highlightbackground="#d9d9d9")
        self.pauseButton.configure(highlightcolor="black")
        self._img1 = tk.PhotoImage(file="./icons/pause.png")
        self.pauseButton.configure(image=self._img1)
        self.pauseButton.configure(pady="0")
        self.pauseButton.configure(text='''Button''')

        self.playButton = tk.Button(top, command=self.play_music)
        self.playButton.place(relx=0.652, rely=0.270, height=38, width=38)
        self.playButton.configure(activebackground="#ececec")
        self.playButton.configure(activeforeground="#000000")
        self.playButton.configure(background="#fff")
        self.playButton.configure(borderwidth="0")
        self.playButton.configure(disabledforeground="#a3a3a3")
        self.playButton.configure(foreground="#000000")
        self.playButton.configure(highlightbackground="#d9d9d9")
        self.playButton.configure(highlightcolor="black")
        self._img2 = tk.PhotoImage(file="./icons/play.png")
        self.playButton.configure(image=self._img2)
        self.playButton.configure(pady="0")
        self.playButton.configure(text='''Button''')

        self.stopButton = tk.Button(top, command=self.stop_music)
        self.stopButton.place(relx=0.725, rely=0.270, height=38, width=38)
        self.stopButton.configure(activebackground="#ececec")
        self.stopButton.configure(activeforeground="#000000")
        self.stopButton.configure(background="#fff")
        self.stopButton.configure(borderwidth="0")
        self.stopButton.configure(disabledforeground="#a3a3a3")
        self.stopButton.configure(foreground="#000000")
        self.stopButton.configure(highlightbackground="#d9d9d9")
        self.stopButton.configure(highlightcolor="black")
        self._img3 = tk.PhotoImage(file="./icons/stop.png")
        self.stopButton.configure(image=self._img3)
        self.stopButton.configure(pady="0")
        self.stopButton.configure(text='''Button''')

        self.previousButton = tk.Button(top, command=self.load_previous_song)
        self.previousButton.place(relx=0.502, rely=0.270, height=36, width=36)
        self.previousButton.configure(background="#fff")
        self.previousButton.configure(borderwidth="0")
        self.previousButton.configure(disabledforeground="#a3a3a3")
        self.previousButton.configure(foreground="#000000")
        self._img5 = tk.PhotoImage(file="./icons/previous.png")
        self.previousButton.configure(image=self._img5)

        self.playList = ScrolledListBox(top)
        self.playList.place(relx=0.0, rely=0.38, relheight=0.532, relwidth=0.999)
        self.playList.configure(background="white")
        self.playList.configure(disabledforeground="#a3a3a3")
        self.playList.configure(font=font11)
        self.playList.configure(foreground="black")
        self.playList.configure(highlightbackground="#d9d9d9")
        self.playList.configure(highlightcolor="#d9d9d9")
        self.playList.configure(selectbackground="#616161")
        self.playList.configure(selectforeground="white")
        self.playList.configure(width=10)

        self.bottomBar = ttk.Label(top)
        self.bottomBar.place(relx=0.0, rely=0.913, height=70, width=1536)
        self.bottomBar.configure(background="#616161")
        self.bottomBar.configure(foreground="#000000")
        self.bottomBar.configure(font="TkDefaultFont")
        self.bottomBar.configure(relief='flat')
        self.bottomBar.configure(width=686)
        self.bottomBar.configure(state='disabled')

        self.vol_scale = ttk.Scale(top)
        self.vol_scale.place(relx=0.035, rely=0.938, relwidth=0.18, relheight=0.0, height=26, bordermode='ignore')
        self.vol_scale.configure(takefocus="")
        self.vol_scale.set(0.5)

        self.addSongsToPlayListButton = tk.Button(top)
        self.addSongsToPlayListButton.place(relx=0.961, rely=0.323, height=18, width=18)
        self.addSongsToPlayListButton.configure(activebackground="#d7eafd")
        self.addSongsToPlayListButton.configure(activeforeground="#d9d9d9")
        self.addSongsToPlayListButton.configure(background="#fff")
        self.addSongsToPlayListButton.configure(borderwidth="0")
        self.addSongsToPlayListButton.configure(disabledforeground="#a3a3a3")
        self.addSongsToPlayListButton.configure(foreground="#000000")
        self.addSongsToPlayListButton.configure(highlightbackground="#d9d9d9")
        self.addSongsToPlayListButton.configure(highlightcolor="black")
        self._img6 = tk.PhotoImage(file="./icons/add.png")
        self.addSongsToPlayListButton.configure(image=self._img6)
        self.addSongsToPlayListButton.configure(pady="0")
        self.addSongsToPlayListButton.configure(text='''Button''')

        self.deleteSongsFromPlaylistButton = tk.Button(top)
        self.deleteSongsFromPlaylistButton.place(relx=0.917, rely=0.323, height=18, width=18)
        self.deleteSongsFromPlaylistButton.configure(activebackground="#fee0e7")
        self.deleteSongsFromPlaylistButton.configure(activeforeground="#000000")
        self.deleteSongsFromPlaylistButton.configure(background="#fff")
        self.deleteSongsFromPlaylistButton.configure(borderwidth="0")
        self.deleteSongsFromPlaylistButton.configure(disabledforeground="#a3a3a3")
        self.deleteSongsFromPlaylistButton.configure(foreground="#000000")
        self.deleteSongsFromPlaylistButton.configure(highlightbackground="#d9d9d9")
        self.deleteSongsFromPlaylistButton.configure(highlightcolor="black")
        self._img7 = tk.PhotoImage(file="./icons/delete.png")
        self.deleteSongsFromPlaylistButton.configure(image=self._img7)
        self.deleteSongsFromPlaylistButton.configure(pady="0")
        self.deleteSongsFromPlaylistButton.configure(text='''Button''')

        self.Button9 = tk.Button(top)
        self.Button9.place(relx=0.933, rely=0.915, height=48, width=48)
        self.Button9.configure(activebackground="#838383")
        self.Button9.configure(activeforeground="#000000")
        self.Button9.configure(background="#616161")
        self.Button9.configure(borderwidth="0")
        self.Button9.configure(disabledforeground="#a3a3a3")
        self.Button9.configure(foreground="#000000")
        self.Button9.configure(highlightbackground="#d9d9d9")
        self.Button9.configure(highlightcolor="black")
        self._img8 = tk.PhotoImage(file="./icons/like.png")
        self.Button9.configure(image=self._img8)
        self.Button9.configure(pady="0")
        self.Button9.configure(text='''Button''')
        self.Button9.configure(width=42)

        self.Button10 = tk.Button(top)
        self.Button10.place(relx=0.874, rely=0.915, height=48, width=48)
        self.Button10.configure(activebackground="#838383")
        self.Button10.configure(activeforeground="#000000")
        self.Button10.configure(background="#616161")
        self.Button10.configure(borderwidth="0")
        self.Button10.configure(disabledforeground="#a3a3a3")
        self.Button10.configure(foreground="#000000")
        self.Button10.configure(highlightbackground="#d9d9d9")
        self.Button10.configure(highlightcolor="black")
        self._img9 = tk.PhotoImage(file="./icons/broken-heart.png")
        self.Button10.configure(image=self._img9)
        self.Button10.configure(pady="0")
        self.Button10.configure(text='''Button''')
        self.Button10.configure(width=48)

        self.Button11 = tk.Button(top)
        self.Button11.place(relx=0.815, rely=0.915, height=48, width=48)
        self.Button11.configure(activebackground="#838383")
        self.Button11.configure(activeforeground="#000000")
        self.Button11.configure(background="#616161")
        self.Button11.configure(borderwidth="0")
        self.Button11.configure(disabledforeground="#a3a3a3")
        self.Button11.configure(foreground="#000000")
        self.Button11.configure(highlightbackground="#d9d9d9")
        self.Button11.configure(highlightcolor="black")
        self._img10 = tk.PhotoImage(file="./icons/refresh.png")
        self.Button11.configure(image=self._img10)
        self.Button11.configure(pady="0")
        self.Button11.configure(text='''Button''')

        self.setup_player()

    def setup_player(self):

        if self.player.get_db_status() is True:
            messagebox.showinfo("Database Connectivity", "Database Connected Successfully !!!")
            self.Button9.config(command=self.add_song_to_favourites)
            self.Button10.config(command=self.remove_song_from_favourites)
            self.Button11.config(command=self.load_song_from_favourites)
        else:
            self.Button9.configure(state="disabled")
            self.Button10.configure(state="disabled")
            self.Button11.configure(state="disabled")
            messagebox.showinfo("Database Connectivity", "Cannot Connect To Database !!!")

        self.playButton.config(command=self.play_music)
        self.pauseButton.config(command=self.pause_music)
        self.stopButton.config(command=self.stop_music)
        self.previousButton.config(command=self.load_previous_song)
        self.addSongsToPlayListButton.config(command=self.add_music)
        self.deleteSongsFromPlaylistButton.config(command=self.delete_music)
        self.playList.bind("<Double-1>", self.list_double_click)
        self.vol_scale.config(command=self.set_volume)
        self.top.protocol("WM_DELETE_WINDOW", self.close_player)

    def add_music(self):
        song_name_list = self.player.add_song()
        for song in song_name_list:
            if song[1] is False:
                self.playList.insert(tk.END, song[0])

    def setup_thread(self):
        self.thread = threading.Thread(target=self.show_timer, args=(self.length, ))
        self.thread.start()

    def show_timer(self, total_sec):
        curr_sec = 0
        progress = 100/total_sec
        self.songProgress.stop()
        while curr_sec < int(total_sec) and mixer.music.get_busy():
            if self.check is False:
                continue
            curr_sec += 1
            length_str = str(int(curr_sec) // 60).zfill(2) + ":" + str(int(curr_sec) % 60).zfill(2)
            self.songTimePassed.config(text=length_str)
            self.songProgress.step(progress)
            time.sleep(1)
        if int(total_sec)-curr_sec == 0:
            self.load_next_song()
        self.thread_running = False

    def load_next_song(self):
        set_next = self.played[0]+1
        size = len(self.playList.get(0, tk.END))
        if set_next > size-1:
            self.playList.select_clear(0, tk.END)
            self.playList.selection_set(0)
            self.play_music()
        else:
            self.playList.select_clear(0, tk.END)
            self.playList.selection_set(set_next)
            self.play_music()

    def play_music(self):
        try:
            self.played = self.playList.curselection()
            if len(self.played) == 0:
                self.played = None
                raise NoSongSelectedError
            if self.thread_running is True:
                self.player.stop_song()
                time.sleep(1)
            song_name = self.playList.get(self.played)
            self.show_song_details(song_name)
            self.player.play_song()
            self.setup_thread()
            self.player.set_volume(self.vol_scale.get())
            self.check = True
            self.thread_running = True

        except NoSongSelectedError:
            messagebox.showinfo("Song Selection", "Please Select A Song To Be Played ...")

    def list_double_click(self, e):
        self.play_music()

    @staticmethod
    def random_color():
        red = hex(random.randint(0, 255))[2:]
        green = hex(random.randint(0, 255))[2:]
        blue = hex(random.randint(0, 255))[2:]

        if len(red) == 1:
            red = "0" + red
        if len(blue) == 1:
            blue = "0" + blue
        if len(green) == 1:
            green = "0" + green

        my_color = "#" + red + green + blue
        return my_color

    def show_song_details(self, song_name):
        self.length = self.player.get_song_length(song_name)
        color = self.random_color()
        self.songName.config(text="%.30s .." % song_name, fg=color)
        length_str = str(int(self.length)//60).zfill(2)+":"+str(int(self.length) % 60).zfill(2)
        self.songTotalDuration.config(text=length_str)

    def pause_music(self):
        if self.check is True:
            self.player.pause_song()
            self.check = False
        else:
            self.player.unpause_song()
            self.check = True

    def stop_music(self):
        self.player.stop_song()
        self.played = None
        self.songName.config(text="MOUZIKKA  ", fg="#616161")
        self.songTotalDuration.config(text="00:00")
        self.songTimePassed.config(text="00:00")
        self.songProgress.stop()
        self.check = False

    def load_previous_song(self):
        if self.played is not None:
            prev_index = self.played[0]-1
            if prev_index < 0:
                self.playList.select_clear(0, tk.END)
                self.playList.selection_set(tk.END)
                self.play_music()
            else:
                self.playList.select_clear(0, tk.END)
                self.playList.selection_set(prev_index)
                self.play_music()

    def set_volume(self, volume):
        self.player.set_volume(float(volume))

    def delete_music(self):
        try:
            selected = self.playList.curselection()
            if len(selected) == 0:
                raise NoSongSelectedError
            if self.played is not None:
                if selected[0] < self.played[0]:
                    self.played = list(self.played)
                    self.played[0] -= 1
                    self.played = tuple(self.played)
                elif selected[0] == self.played[0]:
                    self.stop_music()
            self.player.remove_song(self.playList.get(selected))
            self.playList.delete(selected)

        except NoSongSelectedError:
            messagebox.showinfo("Song Selection", "No Song Selected, Select A Song To Be Deleted  ")

    def close_player(self):
        if messagebox.askyesno("Quit", "Do You Really Want To Quit  ?     "):
            self.player.close_player()
            musicplayer_support.destroy_window()

    def add_song_to_favourites(self):
        try:
            fav_song_index = self.playList.curselection()
            if len(fav_song_index) == 0:
                raise NoSongSelectedError("Please Select A Song ..")
            song_name = self.playList.get(fav_song_index[0])
            result = self.player.add_song_to_favourites(song_name)
            messagebox.showinfo("Add Favourite", result+" ..")

        except NoSongSelectedError as ex:
            messagebox.showinfo("Add Favourite", ex)

    def remove_song_from_favourites(self):
        try:
            fav_song_index = self.playList.curselection()
            if len(fav_song_index) == 0:
                raise NoSongSelectedError("Please Select A Song ..")
            song_name = self.playList.get(fav_song_index[0])
            result = self.player.remove_song_from_favourites(song_name)
            messagebox.showinfo("Remove Favourite", result+" ..")

        except NoSongSelectedError as ex:
            messagebox.showinfo("Remove Favourite", ex)

    def load_song_from_favourites(self):
        try:
            result = self.player.load_song_from_favourites()
            if len(result) == 1:
                raise NoSongSelectedError(result[0])
            self.playList.delete(0, tk.END)
            keys = result[1].keys()
            for song_name in keys:
                self.playList.insert(tk.END, song_name)
            messagebox.showinfo("Load Favourite", result[0]+" ..")

        except NoSongSelectedError as ex:
            messagebox.showinfo("Load Favourite", ex)


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    # Configure the scrollbars for a widget.

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        # self.configure(y_scroll_command=_auto_scroll(vsb),
        #    x_scroll_command =_auto_scroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        # Hide and show scrollbar as needed.
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped


class ScrolledListBox(AutoScroll, tk.Listbox):
    # A standard Tkinter Text widget with scrollbars that will
    # automatically show/hide as needed.
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

# importing platform


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


if __name__ == '__main__':
    vp_start_gui()
