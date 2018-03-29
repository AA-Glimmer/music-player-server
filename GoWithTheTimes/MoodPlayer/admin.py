from django.contrib import admin

# Register your models here.
from .models import usermodel,user_preference,like_song,hate_song,song_metadata

admin.site.register(usermodel)
admin.site.register(user_preference)
admin.site.register(like_song)
admin.site.register(hate_song)
admin.site.register(song_metadata)
