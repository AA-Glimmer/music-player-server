import random

from GoWithTheTimes.recomender import utils
from GoWithTheTimes.recomender.modelupdate import SongModel


class Matcher:
    def __init__(self, songs_handler):
        self.songs_handler = songs_handler

    def _pick_random_song_category(self, user_model):
        # user_model: instance if class UserModel
        # random pick a category based on the preference  of user
        song_category = user_model.song_category.generate_random_song_category()
        return song_category

    # def _filter_hated_songs(self, user_model):
    #     pass

    def _get_songs(self, song_category):
        # song_category: instance of class SongCategory
        # given a specific category of song
        # return a list of song_model
        # TODO return a list of song_model(instance of SongModel) of specific song_category
        self.songs_handler  ## I don not know how to dealt with database
        song_model1 = SongModel()
        song_model2 = SongModel()
        return [song_model1, song_model2]

    def _score_songs(self, user_model, song_models):
        # user_model: instance of class UserModel, song_models: list of instance of class SongModel
        # score all songs in a list, based on the consine of user mood vector and  song mood vector
        # return a score list
        song_scores = map(lambda song_model:
                          utils.find_consine_distance(song_model.vectorize_mood(),
                                                      user_model.vectorize_mood()),
                          song_models)
        return list(song_scores)

    def _pick_random_song(self, song_models, song_scores):
        song_model = random.choice(song_models, weights=song_scores, k=1)
        return song_model

    def recommend_song(self, user_model):
        song_category = self._pick_random_song_category(user_model)
        song_models = self._get_songs(song_category)
        song_scores = self._score_songs()
        song_model_chosen = self._pick_random_song(song_models, song_scores)
        while song_model_chosen.song_id in user_model.song_category.hated_songs:
            song_model_chosen = self._pick_random_song(song_models, song_scores)
        return song_model_chosen.song_id
