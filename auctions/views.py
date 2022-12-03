from email import message
import re
from unicodedata import category
from urllib import request
from webbrowser import get
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django import template
from django.contrib import messages




# register = template.Library()
# @register.filter(name='search')
# def search(value, id):
#     for v in value:
#         if v.id == id:
#             return True
#         return False


def index(request, category_slug=None):
    category=None
    categories = Category.objects.all()
    auctions =Auction.objects.all()
    
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        auctions = auctions.filter(category=category)
        
    return render(request, "auctions/index.html",{"auctions":auctions, "category":category, "categories":categories,})


@login_required
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creator = request.user
            instance.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, "auctions/create.html", {'form' : CreateForm})
    


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

@login_required
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
        if username is not None:

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
    else:
        return render(request, "auctions/register.html")




def listing(request, listing_id):
    try:
        auction = Auction.objects.get(id=listing_id)
        bid = BidForm()
        com = CommentForm()
        # close =CloseForm()
        comments = Comment.objects.filter(auction_id=listing_id)
        
        
            
    except Auction.DoesNotExist:
        raise Http404("Listing not found.")

    return render(request, "auctions/listing.html",{"auction":auction,"bid":bid, "com":com, "comments":comments, })


@login_required
def auction_detail(request, slug):
    auction = get_object_or_404(Auction, slug=slug, is_active=True)
    return render(request, "auctions/listing.html", {"auction": auction})


# def add_watchlist(request, listing_id):
#     try:
#         watchlist = Watchlist.objects.get(pk=listing_id)
        

#     except Watchlist.DoesNotExist:
#         watchlist = None

    
#     user=request.user
#     watchlist.listings.add(user)
#     watchlist.save()
#     return HttpResponseRedirect(reverse("listing", args=(watchlist.id)))

    



    # watchlist = Watchlist.objects.all()
    # auction =get_object_or_404(Auction, pk=auction_id )
    # listing_exist = Watchlist.objects.filter(user=request.user, auction=auction_id)

    # if listing_exist.exists():
    #     message.add_message(request, message.ERROR, "You already have it in your watchlist.")
    #     return HttpResponseRedirect(reverse("watchlist"))

    # watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    # watchlist.listings.add(auction)
    # message.add_message(request, message.SUCCESS, "Successfully added to your watchlist")
    # return HttpResponseRedirect(reverse("watchlist", args=(auction_id,)))
    
        

    # watchlists = Watchlist.objects.all()
    # listing = get_object_or_404(Auction, pk=listing_id )

    # listing_exist = Watchlist.objects.get_or_create(user=request.user, listing=listing)

    # if listing_exist.exists():
    #     message.Error(request, "Item Exist on your watchlist")
    #     return HttpResponseRedirect(reverse("index"))
    # else:
    #     Watchlist.objects.create(user=request.user, listing=listing)

@login_required
def wishlist(request):
    auctions = Auction.objects.filter(wishlist=request.user)
    return render(request, "auctions/wishlist.html", {"wishlist": auctions})
    

@login_required
def add_to_wishlist(request, id):
    auction = get_object_or_404(Auction, id=id)
    watched = auction.wishlist.filter(id=request.user.id).exists()
    if watched:
        auction.wishlist.remove(request.user)
        messages.success(request, auction.title + " has been removed from your WishList")
    else:
        auction.wishlist.add(request.user)
        messages.success(request, "Added " + auction.title + " to your WishList")
    return redirect(request.META["HTTP_REFERER"])


@login_required
def bid(request):
    auction = get_object_or_404(Auction, pk=id)
    bid = BidForm(request.POST or None, request.FILES)
    user = request.user
    if request.method == "POST" and bid.is_valid():
        instance = bid.save(commit=False)
        instance.bidder=user
        instance.bid_price = float(request.POST.get('bid_price'))
        instance.listing_id = Auction.objects.get(id=id)
        if  instance.bid_price >= auction.price:
            if auction.current_bid is None:
                auction.current_bid = instance.bid_price
                auction.buyer = user
                auction.price = instance.bid_price
                instance.save()
                auction.save()
                messages.success(request, "Bid Saved successfully, We will contact you if you win this bid")

            elif instance.bid_price > auction.current_bid:
                auction.current_bid = instance.bid_price
                auction.buyer = user
                # bid.user = user
                # bid.listing_id = auction.id
                auction.price = instance.bid_price
                instance.save()
                auction.save()
                messages.success(request, "Bid Saved successfully, We will contact you if you win this bid")
            
            else:
                messages.error(request, "Bid is lower than current bid")
            
            
        else:
            messages.error(request, " Bid is lower than starting price")
            
    else:
        bid=BidForm()
        return render(request, "auctions/listing.html",{"auction":auction,"bid":bid, })



    return render(request, "auctions/listing.html",{"auction":auction,"bid":bid, })


@login_required
def comments(request, id):
    auction= Auction.objects.get(id=id)
    bid = BidForm()
    com = CommentForm()
    comment = Comment.objects.filter(comment= Auction.objects.get(auction_id=auction.title))
    return render(request, "auctions/listing.html", {"comment": comment, "auction":auction, "bid":bid, "com":com})




@login_required
def comment(request, id):
    auction= get_object_or_404(Auction, pk=id)
    user = request.user
    bid = BidForm()
    com = CommentForm(request.POST, request.FILES)
    # auction = get_object_or_404(Auction, slug= auction)
    # comments = auction.comments.all()
    if request.method == "POST":
        if com.is_valid():
            instance = com.save(commit=False)
            instance.user=user
            instance.auction_id = Auction.objects.get(id=id)
            instance.save()
            messages.success(request, "Comment Saved successfully, We will contact you if you win this bid")
        return HttpResponseRedirect(reverse('listing', args=(auction.id,)))
       
    return render(request, "auctions/listing.html", {'com' : com, "auction":auction, "comments":comments, "bid":bid, "com":com})



@login_required
def closelisting(request, id):
    auction = Auction.objects.get(id=id)
    # close = CloseForm(request.POST, request.FILES)
    bid = BidForm()
    com = CommentForm()
    if request.method == "POST":
        # if close.is_valid():
        if auction.is_active:
            if request.user == auction.creator:
                auction.is_active="False"
                auction.save()
                messages.success(request, "Listing is now inactive")
               
        else:
            messages.error(request, "Listing is currently closed ")
    # else:
        # close = CloseForm()
    
    return render(request, "auctions/listing.html", { "auction":auction, "bid":bid, "com":com })
    