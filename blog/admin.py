from django.contrib import admin
from .models import Post, Comment, Country, Place, Images


admin.site.register(Post)
admin.site.register(Country)
admin.site.register(Place)
admin.site.register(Comment)
admin.site.register(Images)