from django.contrib import admin
from .models import Bid, User, comments,listing,Watchlist
# Register your models here.

admin.site.register(User)
admin.site.register(listing)
admin.site.register(Watchlist)
admin.site.register(comments)
admin.site.register(Bid)