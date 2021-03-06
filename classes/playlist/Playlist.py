# -*- coding: utf-8 -*-
import sys
import os
if os.environ['HOME_BA'] not in sys.path:
    try:
        sys.path.append(os.environ['HOME_BA'])
    except:
        print("error in HOME_BA environment variable")


import time
import datetime
from time import mktime, strptime
import os.path
from random import shuffle
from classes.util.ListDir import ListDir
from classes.content.Trailer import Trailer
from classes.content.LoopedSlide import LoopedSlide
from classes.content.LoopedMovie import LoopedMovie
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class Playlist():

    def __init__(self):
        self.movie_list = []
        self.slide_list = []
        self.playlist = self.make_playlist()
        logging.info("PLAYLIST APRES TOUTES LES INSERTIONS:\n %s" % (self))

    def __str__(self):
        chaine = ""
        for each in self.playlist:
            chaine += str(each) + "\n"
        return chaine

    def make_playlist(self):
        """
        fonction qui fabrique une playlist
        """

        playlist = []

        # lister les fichiers de /var/cine35/trailer et creer les trailers
        self.movie_list = ListDir.list_directory(env_variables.trailer_directory, 'mp4')
        self.slide_list = ListDir.list_directory(env_variables.trailer_directory, 'jpg')

        for each_movie in self.movie_list:
            slidepath = os.path.splitext(each_movie)[0] + '.jpg'
            if slidepath in self.slide_list:
                trailer = Trailer(each_movie, slidepath)
                playlist = trailer.insert(playlist)

        if env_variables.random_play is True:
            shuffle(playlist)

        # inserer les looped_movie
        looped_movies = ListDir.list_directory(env_variables.looped_movie_directory, 'mp4')
        ordered_looped_movies = ListDir.sort_by_start_index(looped_movies)
        for looped_movie_path in ordered_looped_movies:
            movie = LoopedMovie(looped_movie_path)
            playlist = movie.insert(playlist)

        # inserer les looped_slide
        looped_slides = ListDir.list_directory(env_variables.looped_slide_directory, 'jpg')
        ordered_looped_slides = ListDir.sort_by_start_index(looped_slides)
        for looped_slide_path in ordered_looped_slides:
            slide = LoopedSlide(looped_slide_path)
            playlist = slide.insert(playlist)

        return playlist


if __name__ == '__main__':
    my_playlist = Playlist()
    print(my_playlist)

