#This file tests my playlist program automatically.
#It does not use the menu. It calls my classes and methods directly.

#HOW EVERY CHECK WORKS (only one kind of check is used):
#    self.assertEqual means what I got nust be the same with what I expected

import unittest   #Python's built-in testing tool
import os         #used to check for and delete the temporary test file
from unittest.mock import patch   #lets the test type answers for the program

#My main file starts the login as soon as it is imported.
#So while importing, patch gives it fake answers, the login
#fails three times, and the program stops. Then the tests can begin.
with patch("builtins.input", side_effect=["x", "x", "x", "x", "x", "x"]):
    from ENTERPRISE_SOFTWARE_ENG_ASSIGNMENT2 import Song, Playlist, PlaylistManager


#Tests for things that happen inside a playlist
class TestPlaylist(unittest.TestCase):

    #setUp runs before EVERY test, so each test starts with a fresh playlist
    def setUp(self):
        self.playlist = Playlist("Test Playlist")
        self.playlist.add_song(Song("Zebra", "Artist A", "Pop"))
        self.playlist.add_song(Song("Apple", "Artist B", "Jazz"))
        self.playlist.add_song(Song("Mango", "Artist C", "Rock"))

    #method add a song
    def test_add_song(self):
        self.playlist.add_song(Song("Banana", "Artist D", "Pop"))
        #Check: the playlist should now have 4 songs
        self.assertEqual(len(self.playlist.songs), 4)
        #Check: the last song should be called Banana
        self.assertEqual(self.playlist.songs[3].name, "Banana")

    #method sort songs A-Z
    def test_sort_songs(self):
        self.playlist.Sort_Songs()
        names = []
        for song in self.playlist.songs:
            names.append(song.name)
        #Check: the names should now be in A-Z order
        self.assertEqual(names, ["Apple", "Mango", "Zebra"])

    #method change song details
    def test_change_song(self):
        result = self.playlist.Change_Song("Apple", "Apricot", "New Artist", "Soul")
        #the method should say it found the song
        self.assertEqual(result, True)
        #the song's name, artist and genre should be the new ones
        changed_song = self.playlist.songs[1]
        self.assertEqual(changed_song.name, "Apricot")
        self.assertEqual(changed_song.artist, "New Artist")
        self.assertEqual(changed_song.genre, "Soul")

    #method shuffle keeps the same songs (only the order changes)
    def test_shuffle_keeps_all_songs(self):
        self.playlist.Shuffle_Songs()
        names = []
        for song in self.playlist.songs:
            names.append(song.name)
        #there should still be 3 songs
        self.assertEqual(len(names), 3)
        #sorting the names should give the same 3 songs as before
        self.assertEqual(sorted(names), ["Apple", "Mango", "Zebra"])


#Tests for things that happen across all playlists
class TestPlaylistManager(unittest.TestCase):

    def setUp(self):
        self.manager = PlaylistManager()
        self.test_file = "test_export_file.txt"   

    #tearDown runs after every test which deletes the temporary file if it exists
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    #create a playlist
    def test_create_playlist(self):
        self.manager.Create_Playlist("Gym")
        #there should be 1 playlist
        self.assertEqual(len(self.manager.playlists), 1)
        #its name should be Gym
        self.assertEqual(self.manager.playlists[0].name, "Gym")

    #rename a playlist
    def test_rename_playlist(self):
        self.manager.Create_Playlist("Old Name")
        result = self.manager.Rename_Playlist("Old Name", "New Name")
        #the method should say it worked
        self.assertEqual(result, True)
        #the playlist should now be called New Name
        self.assertEqual(self.manager.playlists[0].name, "New Name")

    # remove a playlist (and its songs)
    def test_remove_playlist(self):
        self.manager.Create_Playlist("Gym")
        self.manager.find_playlist("Gym").add_song(Song("Stronger", "Kanye West", "Hip-Hop"))
        result = self.manager.Remove_Playlist("Gym")
        #the method should say it worked
        self.assertEqual(result, True)
        #there should be no playlists left
        self.assertEqual(len(self.manager.playlists), 0)

    #export to a file, then load it back and check it matches
    def test_export_then_load(self):
        self.manager.Create_Playlist("Gym")
        self.manager.find_playlist("Gym").add_song(Song("Stronger", "Kanye West", "Hip-Hop"))
        self.manager.find_playlist("Gym").add_song(Song("Titanium", "David Guetta", "Dance"))
        self.manager.Export_To_File(self.test_file)       

        #the exported file should exist
        self.assertEqual(os.path.exists(self.test_file), True)

        new_manager = PlaylistManager()                  
        result = new_manager.Load_From_File(self.test_file)
        #loading should say it worked
        self.assertEqual(result, True)
        #the loaded playlist should have 2 songs, the first is Stronger
        self.assertEqual(len(new_manager.playlists[0].songs), 2)
        self.assertEqual(new_manager.playlists[0].songs[0].name, "Stronger")


#This line runs all the tests when I run this file directly
if __name__ == "__main__":
    unittest.main()