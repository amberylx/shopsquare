import json, re, subprocess, traceback

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib import auth
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from mall.models import Mall, SSUser, Wishlist, WishlistItem, WishlistImages, Domain
from mall.forms import WishlistItemForm
from utils import urlutils
import MyGlobals    

def wishlist(request, userid):
    form = WishlistItemForm()
    wishlist_dict = _getwishlist(request)
    
    ctx_dict = {
        'ssmedia':'/ssmedia',
        'form':form,
        'all_wishlists':wishlist_dict,
    }
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
    
def _getwishlist(request):
    wishlist_dict = {}
    wishlists = Wishlist.objects.filter(user=request.user)
    for wishlist in wishlists:
        wishlistitems = WishlistItem.objects.filter(wishlist=wishlist)
        wishlistitems_list = _zipWishlistImages(wishlistitems)
        wishlist_dict[wishlist] = wishlistitems_list
    return wishlist_dict
    
def add_to_wishlist(request):
    uid = request.user.id
    url = request.POST.get('url')
    tags = request.POST.get('tags')
    is_private = request.POST.get('is_private', 'off')
    filename = request.POST.get('overlayimagefile')

    wishlistHTML = ''
    successMsg = ''
    errorMsg = ''
    try:
        # add to default wishlist for now
        try:
            wl = Wishlist.objects.get(user=request.user)
        except ObjectDoesNotExist:
            wl = Wishlist(user=request.user, name="default", description="default wishlist")
            wl.save()

        dom = urlutils.getDomainFromUrl(url)
        (domain, created) = Domain.objects.get_or_create(domain=dom)
        wli = WishlistItem(wishlist=wl, url=url, tags=tags, domain=domain, is_private=is_private)
        wli.save()
    except Exception, e:
        status = 'error'
        errorMsg = 'Unable to add %s to your wishlist.' % url
        print "Unable to add %s to wishlist: %s" % (url, str(e))
    else:
        try:
            newfilename = urlutils.getWishlistImageFilename(wli.id)
            oldimgpath = "%s/%s" % (MyGlobals.WISHLISTIMG_ROOT % { 'uid':uid }, filename)
            newimgpath = "%s/%s" % (MyGlobals.WISHLISTIMG_ROOT % { 'uid':uid }, newfilename)
            print "*"*80
            print 'mv %s %s' % (oldimgpath, newimgpath)
            output = subprocess.Popen(['mv %s %s' % (oldimgpath, newimgpath)], shell=True)
            wi = WishlistImages(user=request.user, wishlistitem=wli, path=newfilename)
            wi.save()

            wishlist_dict = _getwishlist(request)
            ctx = {
                'all_wishlists':wishlist_dict
                }
            wishlistHTML = render_to_string("wishlist_snippet.html", ctx, context_instance=RequestContext(request))

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

    # delete wishlistitem image file
    try:
        wlimage = WishlistImages.objects.get(wishlistitem__id=wlitemid)
        imgpath = "%s/%s" % (MyGlobals.WISHLISTIMG_ROOT % { 'uid':uid }, wlimage.path)
        output = subprocess.Popen(['rm %s'%imgpath], shell=True)
    except Exception, e:
        print "unable to delete wishlist image file: %s" % str(e)

    try:
        store = WishlistItem.objects.get(pk=wlitemid)
        store.delete()

        wishlist_dict = _getwishlist(request)
        ctx = {
            'all_wishlists':wishlist_dict
            }
        wishlistHTML = render_to_string("wishlist_snippet.html", ctx, context_instance=RequestContext(request))
        
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
