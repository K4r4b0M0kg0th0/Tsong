import pygame
import os

# Initialize pygame
pygame.init()

# Define the mapping between user commands and actions
COMMANDS = {
    'play': pygame.mixer.music.unpause,
    'pause': pygame.mixer.music.pause,
    'stop': pygame.mixer.music.stop,
    'next': lambda: play_track(current_track + 1),
    'previous': lambda: play_track(current_track - 1),
    'current': lambda: print("Current track:", audio_files[current_track]),
    'skip': lambda: pygame.mixer.music.set_pos(int(input("Enter the time to skip to (in milliseconds): "))),
    'volume up': lambda: pygame.mixer.music.set_volume(min(pygame.mixer.music.get_volume() + 0.1, 1.0)),
    'volume down': lambda: pygame.mixer.music.set_volume(max(pygame.mixer.music.get_volume() - 0.1, 0.0))
}

# Define a function to load and play a track
def play_track(track_index):
    global current_track
    current_track = track_index % len(audio_files)
    try:
        pygame.mixer.music.load(os.path.join(folder_location, audio_files[current_track]))
        pygame.mixer.music.play()
    except pygame.error:
        print("Error loading track:", audio_files[current_track])
        play_track(current_track + 1)

# Get the folder location from the user
folder_location = input("Enter the folder location: ")

# Get a list of all the audio files in the folder
audio_files = [file for file in os.listdir(folder_location) if file.endswith('.mp3')]

# Set the current track to the first track in the list and play it
current_track = 0
play_track(current_track)

# Run the game loop
while True:
    # Check for user input
    command = input("Enter a command (play, pause, stop, next, previous, current, skip, volume up, volume down): ")

    # Check if the command is valid and execute the corresponding action
    if command in COMMANDS:
        COMMANDS[command]()
    else:
        print("Invalid command:", command)
