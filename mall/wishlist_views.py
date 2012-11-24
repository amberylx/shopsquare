import json, re, subprocess, traceback

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from mall.models import Mall, Wishlist, WishlistItem, WishlistImages, Domain
from mall.forms import WishlistItemForm, AddWishlistForm
from utils import urlutils, sysutils
import MyGlobals    

def wishlist(request, userid):
    add_wl_form = AddWishlistForm()
    add_wli_form = WishlistItemForm()
    ctx_dict = _getwishlist(request, userid)
    ctx_dict.update({
        'ssmedia':'/ssmedia',
        'add_wli_form':add_wli_form,
        'add_wl_form':add_wl_form,
    })
    return render_to_response("wishlist.html", ctx_dict, context_instance=RequestContext(request))

def _zipWishlistImages(wishlistitems):
    wishlistitems_list = []
    for wli in wishlistitems:
        try:
            wlimage = WishlistImages.objects.get(wishlistitem=wli)
        except:
            wlimage = None
        wishlistitems_list.append((wli, wlimage))
    return wishlistitems_list
    
def _getwishlist(request, userid):
    wishlist_owner = User.objects.get(pk=userid)
    is_owner = (request.user == wishlist_owner)

    wishlist_dict = {}
    wishlists = Wishlist.objects.filter(user=wishlist_owner)
    for wishlist in wishlists:
        if is_owner:
            wishlistitems = WishlistItem.objects.filter(wishlist=wishlist).order_by("position")
        else:
            wishlistitems = WishlistItem.objects.filter(wishlist=wishlist, is_private=False).order_by("position")
        wishlistitems_list = _zipWishlistImages(wishlistitems)
        wishlist_dict[wishlist] = wishlistitems_list

    ctx_dict = {
        'wishlist_dict':wishlist_dict,
        'wlowner':wishlist_owner,
        'is_owner':is_owner
        }
    return ctx_dict

def _getwishlistHTML(request):
    ctx_dict = _getwishlist(request)
    html = render_to_string("wishlist_snippet.html", ctx_dict, context_instance=RequestContext(request))
    return html
    
def add_wishlist(request):
    name = request.POST.get('name')
    description = request.POST.get('description')

    wishlistHTML = ''
    successMsg = ''
    errorMsg = ''
    try:
        wl = Wishlist(user=request.user, name=name, description=description)
        wl.save()
        wishlistHTML = _getwishlistHTML(request)
        status = 'ok'
    except Exception, e:
        status = 'error'
        errorMsg = 'Unable to create wishlist.'
        print "Unable to create wishlist: %s" % (str(e))
    
    response = {
        'status':status,
        'successMsg':successMsg,
        'errorMsg':errorMsg,
        'wishlistHTML':wishlistHTML
        }
    return HttpResponse(json.dumps(response), mimetype="application/json")

def add_to_wishlist(request):
    uid = request.user.id
    name = "default"
    url = request.POST.get('url')
    tags = request.POST.get('tags')
    is_private = request.POST.get('is_private', 'off')
    filename = request.POST.get('overlayimagefile')

    wishlistHTML = ''
    successMsg = ''
    errorMsg = ''
    try:
        wl = Wishlist.objects.get(user=request.user, name=name)

        dom = urlutils.getDomainFromUrl(url)
        (domain, created) = Domain.objects.get_or_create(domain=dom)
        position = len(WishlistItem.objects.filter(wishlist=wl))
        wli = WishlistItem(wishlist=wl, url=url, tags=tags, domain=domain, is_private=is_private, position=position)
        wli.save()
    except Exception, e:
        status = 'error'
        errorMsg = 'Unable to add %s to your wishlist.' % url
        print "Unable to add %s to wishlist: %s" % (url, str(e))
    else:
        try:
            newfilename = urlutils.getWishlistImageFilename(wli.id)
            sysutils.move_file("%s/%s" % (MyGlobals.WISHLISTIMG_ROOT % { 'uid':uid }, filename),
                               "%s/%s" % (MyGlobals.WISHLISTIMG_ROOT % { 'uid':uid }, newfilename))
            wi = WishlistImages(user=request.user, wishlistitem=wli, path=newfilename)
            wi.save()

            wishlistHTML = _getwishlistHTML(request)
            status = 'ok'
            successMsg = '%s has been added to your wishlist.' % url
        except Exception, e:
            status = 'error'
            error_msg = 'We\'re unable to add image for wishlist item at this time'
            print "unable to save image: %s" % str(e)
            
        
    response = {
        'status':status,
        'successMsg':successMsg,
        'errorMsg':errorMsg,
        'wishlistHTML':wishlistHTML
        }
    return HttpResponse(json.dumps(response), mimetype="application/json")
    
def remove_wishlistitem(request):
    uid = request.user.id
    wlitemid = request.POST.get("wlitemid")
    success_msg = ''
    error_msg = ''
    wishlistHTML = ''

    wlimage = WishlistImages.objects.get(wishlistitem__id=wlitemid)
    sysutils.delete_file("%s/%s" % (MyGlobals.WISHLISTIMG_ROOT % { 'uid':uid }, wlimage.path))

    try:
        store = WishlistItem.objects.get(pk=wlitemid)
        store.delete()

        wishlistHTML = _getwishlistHTML(request)
        status = 'ok'
        success_msg = "Item has been removed from your wishlist."
    except Exception, e:
        print "error removing item: %s" % str(e)
        status = 'error'
        error_msg = "We're sorry, we're unable to remove this item at this time."

    response = {
        'status':status,
        'errorMsg':error_msg,
        'successMsg':success_msg,
        'wishlistHTML':wishlistHTML
        }

    return HttpResponse(json.dumps(response), mimetype="application/json")
