from django.shortcuts import render
from django.http import HttpResponse
from MoodPlayer.models import usermodel,user_preference,like_song,hate_song
from MoodPlayer import utils
from MoodPlayer import songmatcher

# Create your views here.
def PlayerService(request):
    skip = request.GET['skip']
    like = request.GET['like']
    hate = request.GET['hate']
    result = ''
    if(skip == '1'):
        #result = "skipped"
        result = update_model('skip','s001')
    elif(like == '1'):
        #result = "liked"
        result = update_model('like','s001')
    elif(hate == '1'):
        #result = "hated"
        result = update_model('hate','s003')
    else:
        #result = "keep playing"
        result = update_model('hate','s003')
    return HttpResponse(result)

def update_model(reaction, song_id):
    # if the mood of the songs he like always change, then he/she is a mood person.
    # give him/her higher update_rate
    id = 2
    user_usermodel = usermodel.objects.get(user_id=id)
    #retrieve the song meta data

    if reaction == 'like' or reaction == 'no_action':
        if reaction == 'like':
            print("insidelike")
            song_liked = like_song()
            song_liked.user_id = user_usermodel
            song_liked.song_id = song_id
            print(song_liked.song_id)
            song_liked.save()
        #update the usermodel
        if song_songmodel.mood == 'happy':
            user_usermodel.happy = (1-user_usermodel.happy)*0.1 + user_usermodel.happy
            user_usermodel.sad =  user_usermodel.sad - user_usermodel.sad*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry - user_usermodel.angry*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious - user_usermodel.anxious*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving - user_usermodel.loving*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful - user_usermodel.fearful*0.1* 0.2
        elif song_songmodel.mood == 'sad':
            user_usermodel.sad = (1-user_usermodel.sad)*0.1 + user_usermodel.sad
            user_usermodel.happy =  user_usermodel.happy - user_usermodel.happy*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry - user_usermodel.angry*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious - user_usermodel.anxious*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving - user_usermodel.loving*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful - user_usermodel.fearful*0.1* 0.2
        elif song_songmodel.mood == 'angry':
            user_usermodel.angry = (1-user_usermodel.angry)*0.1 + user_usermodel.angry
            user_usermodel.happy =  user_usermodel.happy - user_usermodel.happy*0.1* 0.2
            user_usermodel.sad =  user_usermodel.sad - user_usermodel.sad*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious - user_usermodel.anxious*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving - user_usermodel.loving*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful - user_usermodel.fearful*0.1* 0.2
        elif song_songmodel.mood == 'anxious':
            user_usermodel.anxious = (1-user_usermodel.anxious)*0.1 + user_usermodel.anxious
            user_usermodel.happy =  user_usermodel.happy - user_usermodel.happy*0.1* 0.2
            user_usermodel.sad =  user_usermodel.sad - user_usermodel.sad*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry - user_usermodel.angry*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving - user_usermodel.loving*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful - user_usermodel.fearful*0.1* 0.2
        elif song_songmodel.mood == 'loving':
            user_usermodel.loving = (1-user_usermodel.loving)*0.1 + user_usermodel.loving
            user_usermodel.happy =  user_usermodel.happy - user_usermodel.happy*0.1* 0.2
            user_usermodel.sad =  user_usermodel.sad - user_usermodel.sad*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry - user_usermodel.angry*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious - user_usermodel.anxious*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful - user_usermodel.fearful*0.1* 0.2
        elif song_songmodel.mood == 'fearful':
            user_usermodel.fearful = (1-user_usermodel.fearful)*0.1 + user_usermodel.fearful
            user_usermodel.happy =  user_usermodel.happy - user_usermodel.happy*0.1* 0.2
            user_usermodel.sad =  user_usermodel.sad - user_usermodel.sad*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry - user_usermodel.angry*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious - user_usermodel.anxious*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving - user_usermodel.loving*0.1* 0.2

        user_usermodel.save()
    elif reaction == 'hate' or  reaction == 'skip':
        if reaction == 'hate':
            print("insidehate")
            song_hated = hate_song()
            song_hated.user_id = user_usermodel
            song_hated.song_id = song_id
            print(song_hated.song_id)
            song_hated.save()
            hatesong_fromdb = []
        if song_songmodel.mood == 'happy':
            user_usermodel.happy = user_usermodel.happy - (user_usermodel.happy)*0.1
            user_usermodel.sad =  user_usermodel.sad + (1- user_usermodel.sad)*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry +(1- user_usermodel.angry)*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious + (1-user_usermodel.anxious)*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving + (1-user_usermodel.loving)*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful + (1-user_usermodel.fearful)*0.1* 0.2
        elif song_songmodel.mood == 'sad':
            user_usermodel.sad = user_usermodel.sad - (user_usermodel.sad)*0.1
            user_usermodel.happy =  user_usermodel.happy + (1- user_usermodel.happy)*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry +(1- user_usermodel.angry)*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious + (1-user_usermodel.anxious)*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving + (1-user_usermodel.loving)*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful + (1-user_usermodel.fearful)*0.1* 0.2
        elif song_songmodel.mood == 'angry':
            user_usermodel.angry = user_usermodel.angry - (user_usermodel.angry)*0.1
            user_usermodel.happy =  user_usermodel.happy + (1- user_usermodel.happy)*0.1* 0.2
            user_usermodel.sad =  user_usermodel.sad +(1- user_usermodel.sad)*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious + (1-user_usermodel.anxious)*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving + (1-user_usermodel.loving)*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful + (1-user_usermodel.fearful)*0.1* 0.2
        elif song_songmodel.mood == 'anxious':
            user_usermodel.anxious = user_usermodel.anxious - (user_usermodel.anxious)*0.1
            user_usermodel.happy =  user_usermodel.happy + (1- user_usermodel.happy)*0.1* 0.2
            user_usermodel.sad =  user_usermodel.sad +(1- user_usermodel.sad)*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry + (1-user_usermodel.angry)*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving + (1-user_usermodel.loving)*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful + (1-user_usermodel.fearful)*0.1* 0.2
        elif song_songmodel.mood == 'loving':
            user_usermodel.loving = user_usermodel.loving - (user_usermodel.loving)*0.1
            user_usermodel.happy =  user_usermodel.happy + (1- user_usermodel.happy)*0.1* 0.2
            user_usermodel.sad =  user_usermodel.sad +(1- user_usermodel.sad)*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry + (1-user_usermodel.angry)*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious + (1-user_usermodel.anxious)*0.1* 0.2
            user_usermodel.fearful =  user_usermodel.fearful + (1-user_usermodel.fearful)*0.1* 0.2
        elif song_songmodel.mood == 'fearful':
            user_usermodel.fearful = user_usermodel.fearful - (user_usermodel.fearful)*0.1
            user_usermodel.happy =  user_usermodel.happy + (1- user_usermodel.happy)*0.1* 0.2
            user_usermodel.sad =  user_usermodel.sad +(1- user_usermodel.sad)*0.1* 0.2
            user_usermodel.angry =  user_usermodel.angry + (1-user_usermodel.angry)*0.1* 0.2
            user_usermodel.anxious =  user_usermodel.anxious + (1-user_usermodel.anxious)*0.1* 0.2
            user_usermodel.loving =  user_usermodel.loving + (1-user_usermodel.loving)*0.1* 0.2

        user_usermodel.save()

    else:
        raise Exception

    #update_rate = find_standard_error(liked_songs)
    song_id_chosen = recommend_song(user_usermodel)

    return song_id_chosen

    def recommend_song(user_usermodel):
        song_category = _pick_random_song_category(user_usermodel)
        song_models = _get_songs(song_category)
        song_scores = _score_songs(user_usermodel,song_model_list)
        song_id_chosen = _pick_random_song(song_scores_dict)
        hated_song_list = []
        hatesong_models = hate_song.objects.filter(user_id=user_usermodel)
        #print(hatesong_fromdb)
        for sm in hatesong_models:
            hated_song_list.append(sm.song_id)
        while song_id_chosen in hated_song_list:
            song_id_chosen = _pick_random_song(song_scores_dict)
        return song_id_chosen
