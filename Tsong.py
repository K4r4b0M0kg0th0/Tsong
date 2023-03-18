import pygame
import os
from tkinter import *
from tkinter import ttk

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        master.title("Music Player")

        # Initialize Pygame
        pygame.init()

        # Get the folder location from the user
        self.folder_location = StringVar(value="")
        self.folder_entry = ttk.Entry(master, textvariable=self.folder_location)
        self.folder_entry.grid(row=0, column=0, padx=5, pady=5)
        self.folder_button = ttk.Button(master, text="Open Folder", command=self.load_audio)
        self.folder_button.grid(row=0, column=1, padx=5, pady=5)

        # Set up track navigation buttons
        self.previous_button = ttk.Button(master, text="<<", command=self.previous_track)
        self.previous_button.grid(row=2, column=0, padx=5, pady=5)
        self.next_button = ttk.Button(master, text=">>", command=self.next_track)
        self.next_button.grid(row=2, column=1, padx=5, pady=5)

        # Define the mapping between user commands and actions
        self.COMMANDS = {
            'play': self.play,
            'pause': self.pause,
            'stop': self.stop,
            'skip': self.skip,
            'volume_up': self.volume_up,
            'volume_down': self.volume_down,
        }

        # Set up track information and control labels
        self.current_track_label = ttk.Label(master, text="Currently Playing: None")
        self.current_track_label.grid(row=1, column=0, padx=5, pady=5)
        self.playback_label = ttk.Label(master, text="Playback Controls:")
        self.playback_label.grid(row=3, column=0, padx=5, pady=5)
        self.play_button = ttk.Button(master, text="Play", command=self.play)
        self.play_button.grid(row=4, column=0, padx=5, pady=5)
        self.pause_button = ttk.Button(master, text="Pause", command=self.pause)
        self.pause_button.grid(row=4, column=1, padx=5, pady=5)
        self.stop_button = ttk.Button(master, text="Stop", command=self.stop)
        self.stop_button.grid(row=4, column=2, padx=5, pady=5)
        self.volume_up_button = ttk.Button(master, text="Volume Up", command=self.volume_up)
        self.volume_up_button.grid(row=5, column=0, padx=5, pady=5)
        self.volume_down_button = ttk.Button(master, text="Volume Down", command=self.volume_down)
        self.volume_down_button.grid(row=5, column=1, padx=5, pady=5)
        self.skip_button = ttk.Button(master, text="Skip", command=self.skip)
        self.skip_button.grid(row=5, column=2, padx=5, pady=5)

        # Set default values for variables
        self.audio_files = []
        self.current_track = 0

    def load_audio(self):
        folder_path = self.folder_location.get()
        self.audio_files = [file for file in os.listdir(folder_path) if file.endswith('.mp3')]
        if self.audio_files:
            self.current_track_label.config(text="Currently Playing: {}".format(self.audio_files[self.current_track]))
            self.play()
        else:
            self.current_track_label.config(text="No audio files found in folder.")

    def play_audio(self, track_index):
        try:
            pygame.mixer.music.load(os.path.join(self.folder_location.get(), self.audio_files[track_index]))
            pygame.mixer.music.play()
            self.current_track_label.config(text="Currently Playing: {}".format(self.audio_files[track_index]))
        except pygame.error:
            print("Error loading track:", self.audio_files[track_index])
            self.play_audio(track_index + 1)

    def play(self):
        pygame.mixer.music.unpause()

    def pause(self):
        pygame.mixer.music.pause()

    def stop(self):
        pygame.mixer.music.stop()

    def skip(self):
        time_to_skip = int(input("Enter the time to skip to (in milliseconds): "))
        pygame.mixer.music.set_pos(time_to_skip)

    def volume_up(self):
        current_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(min(current_volume + 0.1, 1.0))

    def volume_down(self):
        current_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(max(current_volume - 0.1, 0.0))

    def next_track(self):
        self.current_track += 1
        self.play_audio(self.current_track % len(self.audio_files))

    def previous_track(self):
        self.current_track -= 1
        self.play_audio(self.current_track % len(self.audio_files))

    def handle_command(self, command_str):
        command = self.COMMANDS.get(command_str, None)
        if command:
            command()
        else:
            print("Invalid command:", command_str)

def main():
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
