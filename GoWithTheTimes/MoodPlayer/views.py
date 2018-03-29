from django.shortcuts import render
from django.http import HttpResponse
from MoodPlayer.models import usermodel,user_preference,like_song,hate_song,song_metadata
from MoodPlayer import utils
from MoodPlayer import songmatcher
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def PlayerService(request):
    skip = request.GET['skip']
    like = request.GET['like']
    hate = request.GET['hate']
    user = request.GET['user']
    createuser = request.GET['createuser']
    userpref = request.GET['userpref']
    result = ''
    user_id = 0
    if(user == '1'):
        username = request.GET['username']
        password = request.GET['password']
        user_id = login_user(request,username,password)
        if(user_id==0):
            result = "Incorrect username or password"
        else:
            result = "logged in successfully"
    if(user_id!=0):
        if(userpref == '1'):
            userpreforder = request.GET['userpreforder']
            result = update_user_preference_model(user_id,userpreforder)
        if(skip == '1'):
            #result = "skipped"
            result = update_model(user_id,'skip','song_102')
        elif(like == '1'):
            #result = "liked"
            result = update_model(user_id,'like','song_102')
        elif(hate == '1'):
            #result = "hated"
            result = update_model(user_id,'hate','song_102')
        else:
            #result = "keep playing"
            result = update_model(user_id,'hate','song_102')
    elif(createuser=='1'):
        username = request.GET['username']
        password = request.GET['password']
        useremail = request.GET['useremail']
        user = User.objects.create_user(username,useremail,password)
        print(user)
        user_usermodel_created = usermodel.objects.create(user_id=user)
        print(user_usermodel_created)
        user_pref_model_created = user_preference.objects.create(user_id=user_usermodel_created)
        result = "new user created"
    else:
        result ="Incorrect username or password"
    return HttpResponse(result)

def login_user(request,username,password):
    luser = authenticate(username = username,password=password)
    if luser is None:
        return 0
    else:
        #luser = User.objects.get(id=luser.id)
        #login(request, luser, backend='django.contrib.auth.backends.ModelBackend')
        return luser.id

def logout_user(request):
    #logout(request)
    return "logged out"

def update_user_preference_model(user_id,userpreforder):
    user_usermodel = usermodel.objects.get(user_id=user_id)
    user_userprefmodel = user_preference.objects.get(user_id=user_usermodel)
    userpreforder_list = userpreforder.split(',')
    if(userpreforder_list[0]=='pop'):
        user_userprefmodel.pop = 0.5
        if(userpreforder_list[1]=='rock'):
            user_userprefmodel.rock=0.3
            user_userprefmodel.rap=0.2
        else:
            user_userprefmodel.rock=0.2
            user_userprefmodel.rap=0.3
    elif(userpreforder_list[0]=='rock'):
        user_userprefmodel.rock = 0.5
        if(userpreforder_list[1]=='pop'):
            user_userprefmodel.pop=0.3
            user_userprefmodel.rap=0.2
        else:
            user_userprefmodel.pop=0.2
            user_userprefmodel.rap=0.3
    elif(userpreforder_list[0]=='rap'):
        user_userprefmodel.rap = 0.5
        if(userpreforder_list[1]=='rock'):
            user_userprefmodel.rock=0.3
            user_userprefmodel.pop=0.2
        else:
            user_userprefmodel.rock=0.2
            user_userprefmodel.pop=0.3
    user_userprefmodel.save()

    return "updated user preference"




def recommend_song(user_usermodel):
    print("inside recommend_song")
    song_category = songmatcher._pick_random_song_category(user_usermodel)
    print(song_category[0])
    song_model_list = songmatcher._get_songs(song_category[0])
    print(song_model_list)
    song_scores_dict = songmatcher._score_songs(user_usermodel,song_model_list)
    print(song_scores_dict)
    song_id_chosen_list = songmatcher._pick_random_song(song_scores_dict)
    print(song_id_chosen_list)
    song_id_chosen = song_id_chosen_list[0]
    hated_song_list = []
    hatesong_models = hate_song.objects.filter(user_id=user_usermodel)
    print("reached hate song checks")
    #print(hatesong_fromdb)
    for sm in hatesong_models:
        hated_song_list.append(sm.song_id)
    while song_id_chosen in hated_song_list:
        song_id_chosen_list = songmatcher._pick_random_song(song_scores_dict)
        song_id_chosen = song_id_chosen_list[0]
    return song_id_chosen


def update_model(user_id,reaction, song_id):
    # if the mood of the songs he like always change, then he/she is a mood person.
    # give him/her higher update_rate
    id = user_id
    print(user_id)
    user_usermodel = usermodel.objects.get(user_id=id)
    #retrieve the song meta data
    song_songmodel = song_metadata.objects.get(song_id=song_id)

    if reaction == 'like' or reaction == 'no_action':
        if reaction == 'like':
            print("insidelike")
            song_liked = like_song()
            song_liked.user_id = user_usermodel
            song_liked.song_id = song_songmodel
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
            song_hated.song_id = song_songmodel
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
    print(song_id_chosen)
    song_songmodel_chosen = song_metadata.objects.get(id=song_id_chosen)

    return [song_songmodel_chosen.song_id,song_songmodel_chosen.path]
