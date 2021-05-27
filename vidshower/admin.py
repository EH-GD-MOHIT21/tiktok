from django.contrib import admin

# Register your models here.

from .models import videodisplayer as vdp,usermodellikedvideoslist as umlv

admin.site.register(vdp)
admin.site.register(umlv)