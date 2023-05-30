from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import RemoteUserBackend
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Watchlist, comments, listing, Bid

def index(request):
    return render(request, "auctions/index.html", {
        "auctions":listing.objects.all(),
        "bids":Bid.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":

        if not request.user.is_authenticated:
            return render(request, "auctions/create.html", {
                "message":"You must be logged in to visit this page"
            })

        user = request.user

        title = request.POST['title']

        desc = request.POST['desc']

        bid = request.POST['bid']

        url = request.POST['url']

        category = request.POST['category']

        if title=="" or bid=="" or desc=="":
            return render(request,"auctions/create.html", {
                "alert":"Please compile all required fields(*)"
            })
        
        l = listing.objects.create(user=user, title=title, desc=desc, price=bid, url=url, category=category)
        l.save()


    return render(request, "auctions/create.html")

def auction(request, auction_id):
    
    l = listing.objects.filter(id=auction_id).first()
    c = comments.objects.filter(listing_id=auction_id)
    b = Bid.objects.filter(listing_id=auction_id).first()
    

    
    if request.user.is_authenticated:
        w = Watchlist.objects.filter(user=request.user, listing=l).first()
        c = comments.objects.filter(listing_id=auction_id)
        b = Bid.objects.filter(listing_id=auction_id).first()
        

        if request.method == "POST":

            a = listing.objects.get(id=auction_id)
        

            

        

            
            
           
            
            comment = request.POST['content' ] 

            if comment=="":
                return render(request, "auctions/listing.html",{
                    "alert1": "You forgot to write something!"
                })
            c = comments.objects.create(content=comment, user=request.user, listing = l)
            c.save()
            return HttpResponseRedirect(f"{auction_id}")

        if w is  None:
            a = True
        else:
            a = False
        return render(request, "auctions/listing.html", {
            "m":b,
            "auction":l,
            "v":w,
            "a":a ,
            "comments":c  })
    return render(request, "auctions/listing.html", {
        "m":b,
        "auction":l,
        "comments":c
    })

@login_required
def watchlist(request):
    user = request.user
    w = Watchlist.objects.filter(user=user)
    return render(request,"auctions/watchlist.html", {
        "watchlist":w
    })

def ARWatch(request, auction_id):

    user = request.user
    l = listing.objects.filter(id = auction_id).first()
    
    w = Watchlist.objects.filter(user = user, listing = l).first()
    
    if w is None:
        wl = Watchlist.objects.create(user = user,listing = l)
        wl.save()
        return HttpResponseRedirect(reverse("watchlist"))
    
    w.delete()
    return HttpResponseRedirect(reverse("watchlist"))

def categories(request):
   g=[]
   l = listing.objects.all()

   for auction in l:
     if auction.category:
        if auction.category not in g:
            g.append(auction.category)
    
   return render(request, "auctions/categories.html", {
        "listings": g
    })


def category_listing(request, category):

    c = category
    l = listing.objects.filter(category=category)
    return render(request, "auctions/category_listing.html", {
        "listings":l,
        "category":c,
    })



    
def auctionClosed(request, auction_id):
    if request.method == "GET":
        a = listing.objects.get(id=auction_id)
        a.closed = True
        a.save()
    return HttpResponse("AUCTION CLOSED")

def newBid(request, auction_id):

    b = Bid.objects.filter(listing_id=auction_id).first()

    if request.method == "POST":

        a = listing.objects.get(id=auction_id)
        

        b = Bid.objects.filter(listing_id=auction_id).first()

        if b is  None:
            
            nowBid = int(a.price)

            newBid = int(request.POST['newBid'])

            

            if nowBid < newBid:
                h = Bid.objects.create(user=request.user, listing_id=auction_id, price=newBid)
                
                h.save()
                return HttpResponse("BID SENT")
            elif nowBid >= newBid:
                return HttpResponse("THE BID MUST BE HIGHER THAN THE PREVIOUS ONE")

        elif b is not None:

            firstbid = int(b.price)
            
            
            secondbid = int(request.POST['newBid'])

            if secondbid <= firstbid:
                return HttpResponse("THE BID MUST BE HIGHER THAN THE PREVIOUS ONE")
            elif secondbid > firstbid:
                g = Bid.objects.filter(listing_id=auction_id).delete()
                
                f=Bid.objects.create(user=request.user, listing_id=auction_id, price=secondbid)
                f.save()
        
                return HttpResponse("BID SENT")
    
   