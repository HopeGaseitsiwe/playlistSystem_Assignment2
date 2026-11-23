#This file includes python libraries that I used in my playlist console
import random #used in the shuffling playlist method
import unittest #for testing the file (tests are written in a separate file)
import os #for checking files


#User login authentication with 3 maximum login tries
class Authenticator:
    valid_username = "user123"
    valid_password = "Givemetheykey123"
    max_attempts = 3

    def login(self):
        attempts = 0
        while attempts < 3:
            username = input("Username: ")
            password = input("Password: ")
            if username == "user123" and password == "Givemetheykey123":
                print("Welcome user123.")
                return True
            attempts = attempts + 1
            print("Invalid attempt. Try again. Tries left:", 3 - attempts)
        print("User has had 3 failed attempts. Try again after 5 minutes.")
        return False

#This class stores the details of one song
class Song:
    def __init__(self, name, artist, genre):
        self.name = name
        self.artist = artist
        self.genre = genre

#Used for sorting A-Z: returns an item's name in lowercase
def get_name(item):
    return item.name.lower()

#This class is one playlist: a name and a list of songs
class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    #This method adds a song to the playlist
    def add_song(self, song):
        self.songs.append(song)

    # This method Changes the song's details
    def Change_Song(self, old_name, new_name, new_artist, new_genre):
        for song in self.songs:
            if song.name.lower() == old_name.lower():
                song.name = new_name
                song.artist = new_artist
                song.genre = new_genre
                return True
        return False

    #This method removes a song with a particular name
    def Remove_Song(self, song_name):
        for song in self.songs:
            if song.name.lower() == song_name.lower():
                self.songs.remove(song)
                return True
        return False

    #This method sorts songs in ascending (A-Z) order
    def Sort_Songs(self):
        self.songs.sort(key=get_name)

    #This method shuffles the songs into a random order
    def Shuffle_Songs(self):
        random.shuffle(self.songs)

    #This method turns the playlist into one line of text for the file
    def to_line(self):
        parts = []
        for song in self.songs:
            parts.append(song.name + "; " + song.artist + "; " + song.genre)
        return self.name + ": " + " | ".join(parts)

#This class keeps all the playlists and works on them
class PlaylistManager:

    def __init__(self):
        self.playlists = []

    def find_playlist(self, name):
        for playlist in self.playlists:
            if playlist.name.lower() == name.lower():
                return playlist
        return None

    #This method creates a new empty playlist
    def Create_Playlist(self, name):
        self.playlists.append(Playlist(name))

    #This method renames a playlist
    def Rename_Playlist(self, old_name, new_name):
        playlist = self.find_playlist(old_name)
        if playlist is None:
            return False
        playlist.name = new_name
        return True

    #This method removes a playlist and all its songs
    def Remove_Playlist(self, name):
        playlist = self.find_playlist(name)
        if playlist is None:
            return False
        self.playlists.remove(playlist)
        return True

    #This method finds songs that appear in more than one playlist
    def Find_Duplicates(self):
        found = {}   # song name -> list of playlist names it is in
        for playlist in self.playlists:
            for song in playlist.songs:
                key = song.name.lower()
                if key not in found:
                    found[key] = []
                found[key].append(playlist.name)

        any_duplicates = False
        for song_name in found:
            if len(found[song_name]) > 1:
                print(song_name, "is in:", ", ".join(found[song_name]))
                any_duplicates = True
        if not any_duplicates:
            print("No duplicate songs found.")

    #This method sorts the playlists A-Z by name
    def Sort_Playlist(self):
        self.playlists.sort(key=get_name)

    #This method sorts the songs inside every playlist A-Z
    def Sort_All_Songs(self):
        for playlist in self.playlists:
            playlist.Sort_Songs()

    #This method shuffles the songs inside every playlist
    def Shuffle_All_Songs(self):
        for playlist in self.playlists:
            playlist.Shuffle_Songs()

    #This method reads playlists from a text file
        #This method reads playlists from a text file
    def Load_From_File(self, filename):
        # Step 1: stop if the file does not exist
        if not os.path.exists(filename):
            return False

        file = open(filename, "r")
        all_lines = file.readlines()
        file.close()

        for line in all_lines:
            line = line.strip()          

            if line == "":               
                continue
            if ":" not in line:          
                continue

           
            playlist_name, songs_text = line.split(":", 1)
            playlist = Playlist(playlist_name.strip())

            song_list = songs_text.split("|")

            for song_text in song_list:
                details = song_text.split(";")
                if len(details) == 3:    # only use songs with all 3 details
                    name = details[0].strip()
                    artist = details[1].strip()
                    genre = details[2].strip()
                    new_song = Song(name, artist, genre)
                    playlist.add_song(new_song)

            self.playlists.append(playlist)
        return True

    #This method writes all playlists to a text file, one playlist per line
    def Export_To_File(self, filename):
        with open(filename, "w") as file:
            for playlist in self.playlists:
                file.write(playlist.to_line() + "\n")

    #This method prints every playlist with its songs
    def Show_All(self):
        if len(self.playlists) == 0:
            print("No playlists yet.")
        for playlist in self.playlists:
            print(playlist.to_line())

#Main menu screen
def show_menu():
    print("\n---Playlist Menu---")
    print("1. Load playlists from a file")
    print("2. Create playlist")
    print("3. Add song to playlist")
    print("4. Change song details")
    print("5. Remove song from playlist")
    print("6. Rename playlist")
    print("7. Delete playlist")
    print("8. Find duplicate songs")
    print("9. Sort playlists")
    print("10. Sort songs")
    print("11. Shuffle songs")
    print("12. Export playlists to file")
    print("13. Show all playlists")
    print("0. Exit")

def main():
    auth = Authenticator()
    if not auth.login():
        return

    manager = PlaylistManager()

    while True:
        show_menu()
        choice = input("Choose an option: ")

        #Sequences of choosing options
        if choice == "1":
            if manager.Load_From_File(input("File name to load: ")):
                print("Playlists loaded:")
                manager.Show_All()
            else:
                print("File not found.")

        elif choice == "2":
            manager.Create_Playlist(input("New playlist name: "))
            print("Playlist created.")

        elif choice == "3":
            playlist = manager.find_playlist(input("Playlist name: "))
            if playlist is None:
                print("Playlist not found.")
            else:
                name = input("Song name: ")
                artist = input("Artist: ")
                genre = input("Genre: ")
                playlist.add_song(Song(name, artist, genre))
                print("Song added.")

        elif choice == "4":
            playlist = manager.find_playlist(input("Playlist name: "))
            if playlist is None:
                print("Playlist not found.")
            else:
                old_name = input("Song to change: ")
                new_name = input("New song name: ")
                new_artist = input("New artist: ")
                new_genre = input("New genre: ")
                if playlist.Change_Song(old_name, new_name, new_artist, new_genre):
                    print("Song changed.")
                else:
                    print("Song not found.")

        elif choice == "5":
            playlist = manager.find_playlist(input("Playlist name: "))
            if playlist is None:
                print("Playlist not found.")
            elif playlist.Remove_Song(input("Song to remove: ")):
                print("Song removed.")
            else:
                print("Song not found.")

        elif choice == "6":
            old_name = input("Playlist to rename: ")
            new_name = input("New name: ")
            if manager.Rename_Playlist(old_name, new_name):
                print("Playlist renamed.")
            else:
                print("Playlist not found.")

        elif choice == "7":
            if manager.Remove_Playlist(input("Playlist to delete: ")):
                print("Playlist deleted.")
            else:
                print("Playlist not found.")

        elif choice == "8":
            manager.Find_Duplicates()

        elif choice == "9":
            print("\nBefore sorting:")
            manager.Show_All()
            manager.Sort_Playlist()
            print("\nAfter sorting playlists A-Z:")
            manager.Show_All()

        elif choice == "10":
            print("\nBefore sorting:")
            manager.Show_All()
            manager.Sort_All_Songs()
            print("\nAfter sorting songs A-Z in each playlist:")
            manager.Show_All()

        elif choice == "11":
            print("\nBefore shuffling:")
            manager.Show_All()
            manager.Shuffle_All_Songs()
            print("\nAfter shuffling songs in each playlist:")
            manager.Show_All()

        elif choice == "12":
            manager.Export_To_File(input("File name to save: "))
            print("Exported.")

        elif choice == "13":
            manager.Show_All()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()