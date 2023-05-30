from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("buttonWL/<int:auction_id>", views.ARWatch, name="ARWatch"),
    path("categories", views.categories, name="categories"),
    path("listing/<str:category>", views.category_listing, name="category_listing"),
    path("bid/<int:auction_id>", views.newBid, name="newBid"),
    path("auctionClosed/<int:auction_id>", views.auctionClosed, name="auctionClosed"),
    
    
]
