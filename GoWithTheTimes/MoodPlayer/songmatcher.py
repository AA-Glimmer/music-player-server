from MoodPlayer.models import usermodel,user_preference,like_song,hate_song,song_metadata
from MoodPlayer import utils
import random

def _get_songs(song_category):
        # song_category: instance of class SongCategory
        # given a specific category of song
        # return a list of song_model
        # TODO return a list of song_model(instance of SongModel) of specific song_category
        #songs_list = usermodel.objects.get()
        #self.songs_handler  ## I don not know how to dealt with database
        #song_model1 = SongModel()
        #song_model2 = SongModel()
        #return [song_model1, song_model2]
        song_model_list = song_metadata.objects.filter(genre=song_category)
        return song_model_list

def _score_songs(user_model, song_model_list):
        # user_model: instance of class UserModel, song_models: list of instance of class SongModel
        # score all songs in a list, based on the consine of user mood vector and  song mood vector
        # return a score list
        user_mood_vector =[]
        user_mood_vector.append(user_model.happy)
        user_mood_vector.append(user_model.sad)
        user_mood_vector.append(user_model.angry)
        user_mood_vector.append(user_model.anxious)
        user_mood_vector.append(user_model.loving)
        user_mood_vector.append(user_model.fearful)
        song_scores_dict = {}
        for song_model in song_model_list:
            song_mood_vector =[]
            if (song_model.mood == 'happy'):
                song_mood_vector.append(1)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
            elif(song_model.mood == 'sad'):
                song_mood_vector.append(0)
                song_mood_vector.append(1)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
            elif(song_model.mood == 'angry'):
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(1)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
            elif(song_model.mood == 'anxious'):
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(1)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
            elif(song_model.mood == 'loving'):
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(1)
                song_mood_vector.append(0)
            elif(song_model.mood == 'fearful'):
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(1)
            else:
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
                song_mood_vector.append(0)
            song_scores = utils.find_consine_distance(song_mood_vector,user_mood_vector)
            song_scores_dict[song_model.id]=song_scores
        return song_scores_dict

def _pick_random_song(song_scores_dict):
        song_id = random.choices(list(song_scores_dict.keys()), weights=list(song_scores_dict.values()), k=1)
        return song_id

def generate_random_song_category(user_usermodel):
        user_pref = user_preference.objects.get(user_id=user_usermodel)
        pref1 = user_preference()
        pref1.pop = 1
        pref1.rock=0
        pref1.rap=0
        pref2 = user_preference()
        pref2.pop = 0
        pref2.rock=1
        pref2.rap=0
        pref3 = user_preference()
        pref3.pop = 0
        pref3.rock=0
        pref3.rap=1
        return random.choices(["pop",
                               "rock",
                               "rap", ],
                              weights=[user_pref.pop, user_pref.rock, user_pref.rap], k=1)

def _pick_random_song_category(user_usermodel):
        # user_model: instance if class UserModel
        # random pick a category based on the preference  of user
        print("inside _pick_random_song_category")
        song_category = generate_random_song_category(user_usermodel)
        return song_category
