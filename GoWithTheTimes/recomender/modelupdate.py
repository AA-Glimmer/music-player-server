import random

from GoWithTheTimes.recomender.utils import find_standard_error


class SongCategory:
    def __init__(self, pop=1, rock=1, jazz=1):
        _sum = pop + rock + jazz
        self.pop = pop / float(_sum)
        self.rock = rock / float(_sum)
        self.jazz = jazz / float(_sum)

    def generate_random_song_category(self):
        return random.choices([SongCategory(pop=1, rock=0, jazz=0),
                               SongCategory(pop=0, rock=1, jazz=0),
                               SongCategory(pop=0, rock=0, jazz=1), ],

                              weights=[self.pop, self.rock, self.jazz], k=1)


class Mood:
    def __init__(self, happy=0.5, sad=0.5, angry=0.5, anxious=0.5, loving=0.5, fearful=0.5):
        self.happy = happy
        self.sad = sad
        self.angry = angry
        self.anxious = anxious
        self.loving = loving
        self.fearful = fearful

    def vectorize(self):
        mood_vector = []
        mood_vector.append(self.happy)
        mood_vector.append(self.sad)
        mood_vector.append(self.angry)
        mood_vector.append(self.anxious)
        mood_vector.append(self.loving)
        mood_vector.append(self.fearful)
        return mood_vector


DEFAULT_UPDATE_RATE = 0.1


class UserModel:
    def __init__(self, user_id, song_category, mood, update_rate=DEFAULT_UPDATE_RATE, counter=0,
                 likeed_songs=None, hated_songs=None):
        self.user_id = user_id
        self.song_category = song_category
        self.mood = mood
        self.update_rate = update_rate
        self.counter = counter

        self.liked_songs = likeed_songs if likeed_songs is not None else []
        self.hated_songs = hated_songs if hated_songs is not None else []

    def vectorize_mood(self):
        return self.mood.vectorize()

    def update_model(self, reaction, song_model):
        # if the mood of the songs he like always change, then he/she is a mood person.
        # give him/her higher update_rate
        if reaction == 'like':
            self.liked_songs.append(song_model.get_id())
            # TODO
        elif reaction == 'hate':
            self.hated_songs.append(song_model.get_id())
            # TODO
        elif reaction == 'no_action':
            # TODO
            pass
        elif reaction == 'skip':
            # TODO
            pass
        else:
            raise Exception

        self.update_rate = find_standard_error(self.liked_songs)

        return self


class SongModel:
    def __init__(self, song_id, song_category, mood):
        # check song taged fine
        def _check(song_category):
            # TODO
            return True

        if not _check(song_category):
            raise Exception
        self.song_id = song_id
        self.song_category = song_category
        self.mood = mood

    def get_id(self):
        return self.song_id

    def vectorize_mood(self):
        return self.mood.vectorize()


if __name__ == '__main__':
    # song1 = SongCategory()
    # mood1 = Mood()
    # user1 = UserModel(song1, mood1)
    # songm1 = SongModel(song1, mood1)
    # print(mood1.vectorize())
    # print(songm1.vectorize_mood())
    pass
