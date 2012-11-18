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
from mall.models import Store, StoreImages, Mall, SSUser, Wishlist, WishlistItem, WishlistImages, Domain
from mall.forms import RegisterForm, AddStoreForm, WishlistItemForm
from utils import ImageScraper, slugify, imageutils, urlutils
import MyGlobals

def landing(request):
    ctx_dict = {
    	'request':request,
    	'ssmedia':'/ssmedia',
    }
    return render_to_response('landing.html', ctx_dict, context_instance=RequestContext(request))

@login_required
def mall(request, mall_id):
    form = AddStoreForm()
    stores_dict = _getmall(mall_id)
    mall = Mall.objects.get(pk=mall_id)
    
    ctx_dict = {
    	'form':form,
    	'mall':mall,
    	'stores_dict':stores_dict,
    	'request':request,
    	'ssmedia':'/ssmedia',
        'MyGlobals':MyGlobals
    }
    return render_to_response("mall.html", ctx_dict, context_instance=RequestContext(request))

def _getmall(mall_id):
    mall = Mall.objects.get(pk=mall_id)
    all_stores = Store.objects.filter(mall__id=mall_id).order_by('floor', 'position')
    stores_dict = {}
    for store in all_stores:
        try:
            si = StoreImages.objects.get(store=store)
        except:
            si = None

        try:
            stores_dict[store.floor].append((store, si))
        except:
            stores_dict[store.floor] = [(store, si)]

    # add extra floor (next expansion)
    all_floors = stores_dict.keys()
    if not all_floors:
        stores_dict[0] = []
    else:
        all_floors.sort()
        stores_dict[all_floors[-1]+1] = []
            
    return stores_dict

def scrape_image(request):
    url = request.POST.get('url')
    scrape_for = request.POST.get('type')
    uid = request.user.id

    imgHTML = ''
    filename = urlutils.getScrapedImageFilename()
    if scrape_for == 'store':
        filedir = MyGlobals.STOREIMG_ROOT % { 'uid':uid }
        imgpath = MyGlobals.STOREIMG_ROOT_SRV % { 'uid':uid }
    elif scrape_for == 'wishlist':
        filedir = MyGlobals.WISHLISTIMG_ROOT % { 'uid':uid }
        imgpath = MyGlobals.WISHLISTIMG_ROOT_SRV % { 'uid':uid }

    try:
        (filedir, filename) = ImageScraper.getImagesFromURL(url, filedir=filedir, filename=filename)
        if filename:
            try:
                (filedir, filename) = imageutils.resize_image(filedir, filename)
            except Exception, e:
                print "unable to resize image: %s" % str(e)
            imgHTML = '<img src="%s/%s"></img>' % (imgpath, filename)
        else:
            raise Exception("no image to scrape")
        status = 'ok'
    except Exception, e:
        print "unable to scrape image: %s; %s" % (str(e), traceback.print_exc())
        filename = None
        imgpath = None
        status = 'error'

    response = {
        'status':status,
        'filename':filename,
        'imgpath':imgpath,
        'imgHTML':imgHTML
        }
    return HttpResponse(json.dumps(response), mimetype="application/json")

def do_crop(request):
    uid = request.user.id
    filename = request.POST.get('filename')
    crop_for = request.POST.get('type')
    crop_x1 = int(float(request.POST.get('crop_x1')))
    crop_y1 = int(float(request.POST.get('crop_y1')))
    crop_x2 = int(float(request.POST.get('crop_x2')))
    crop_y2 = int(float(request.POST.get('crop_y2')))
    cropbox = [crop_x1, crop_y1, crop_x2, crop_y2]

    if crop_for == 'store':
        filedir = MyGlobals.STOREIMG_ROOT % { 'uid':uid }
        imgpath = MyGlobals.STOREIMG_ROOT_SRV % { 'uid':uid }
    elif crop_for == 'wishlist':
        filedir = MyGlobals.WISHLISTIMG_ROOT % { 'uid':uid }
        imgpath = MyGlobals.WISHLISTIMG_ROOT_SRV % { 'uid':uid }
    
    try:
        (filedir, filename) = imageutils.crop_image(filedir, filename, cropbox)
        imgHTML = '<img src="%s/%s"></img>' % (imgpath, filename)
        status = 'ok'
    except Exception, e:
        print "unable to do crop: %s" % str(e)
        status = 'error'
        filename = ''
        imgHTML = ''

    response = {
        'status':status,
        'filename':filename,
        'imgHTML':imgHTML
        }
    return HttpResponse(json.dumps(response), mimetype="application/json")
    
def add_store(request):
    uid = request.user.id
    mallid = request.POST.get('mallid')
    name = request.POST.get('name')
    url = request.POST.get('url')
    tags = request.POST.get('tags')
    filename = request.POST.get('overlayimagefile')

    mallHTML = ''
    success_msg = ''
    error_msg = ''
    try:
        floor = 0
        pos = len(Store.objects.filter(mall__id=mallid, floor=0).order_by('position'))
        dom = urlutils.getDomainFromUrl(url)
        (domain, created) = Domain.objects.get_or_create(domain=dom)
        new_store = Store.objects.create(mall=Mall.objects.get(pk=mallid),
                                         name=name,
                                         url=url,
                                         floor=floor,
                                         position=pos,
                                         tags=tags,
                                         domain=domain)
        new_store.save()
    except Exception, e:
        status = 'error'
        error_msg = 'We\'re unable to add the store %s at this time' % name
        print "unable to create store: %s" % str(e)
    else:
        try:
            newfilename = urlutils.getStoreImageFilename(name, new_store.id)
            oldimgpath = "%s/%s" % (MyGlobals.STOREIMG_ROOT % { 'uid':uid }, filename)
            newimgpath = "%s/%s" % (MyGlobals.STOREIMG_ROOT % { 'uid':uid }, newfilename)
            print "*"*80
            print 'mv %s %s' % (oldimgpath, newimgpath)
            output = subprocess.Popen(['mv %s %s' % (oldimgpath, newimgpath)], shell=True)
            si = StoreImages(user=request.user, store=new_store, path=newfilename)
            si.save()

            stores_dict = _getmall(mallid)
            ctx = {
                'stores_dict':stores_dict
                }
            mallHTML = render_to_string("mall_snippet.html", ctx, context_instance=RequestContext(request))

            status = 'ok'
            success_msg = 'Successfully added store.'
        except Exception, e:
            status = 'error'
            error_msg = 'We\'re unable to add the store %s at this time' % name
            print "unable to save image: %s" % str(e)

    response = {
        'status':status,
        'successMsg':success_msg,
        'errorMsg':error_msg,
        'mallHTML':mallHTML
        }
    return HttpResponse(json.dumps(response), mimetype="application/json")

def move_store(request):
    mallid = request.POST.get("mallid")
    storeid = request.POST.get("storeid")
    movetype = request.POST.get("movetype")
    oldfloorid = request.POST.get("oldfloorid")
    newfloorid = request.POST.get("newfloorid")
    oldfloororder = [re.sub('store=', '', s) for s in request.POST.get("oldfloororder").split('&')]
    newfloororder = [re.sub('store=', '', s) for s in request.POST.get("newfloororder").split('&')]

    error_msg = ''
    try:
        mystore = Store.objects.get(pk=storeid)
        print ".........moving store (storeid: %s, storename: %s, oldfloorid: %s, newfloorid: %s)..........." % (storeid, mystore.name, oldfloorid, newfloorid)
        print ".........(oldfloororder: %s, newfloororder: %s)..........." % (oldfloororder, newfloororder)
        if movetype == 'samefloor':
            print "(samefloor)"
            for x,store in enumerate(newfloororder):
                # iterate through new order. for every store that has changed, update to its new position
                if oldfloororder[x] != store:
                    s = Store.objects.get(pk=store, mall__id=mallid)
                    s.position = x
                    s.save()
                    print "  (samefloor) moving store (#%s) %s to position %s" % (s.id, s.name, s.position)
        elif movetype == 'difffloor':
            print "(difffloor)"
            do_shift = False
            for x,store in enumerate(oldfloororder):
                # iterate over old floor, shift all stores following moved store
                print "(iterate over old floor, shift all stores following moved store)"
                if do_shift:
                    s = Store.objects.get(pk=store, mall__id=mallid)
                    s.position = s.position - 1
                    s.save()
                    print "  (difffloor oldfloor) moving store (#%s) %s to position %s" % (s.id, s.name, s.position)
                if int(oldfloororder[x]) == mystore.id:
                    do_shift = True
                    continue

            do_shift = False
            for x,store in enumerate(newfloororder):
                print "(iterate over new floor, shift all stores following moved store)"
                # iterate over new floor, shift all stores following moved store
                if do_shift:
                    s = Store.objects.get(pk=store, mall__id=mallid)
                    s.position = x
                    s.save()
                    print "  (difffloor newfloor) moving store (#%s) %s to position %s" % (s.id, s.name, s.position)
                if int(newfloororder[x]) == mystore.id:
                    do_shift = True
                    s = mystore
                    s.floor = newfloorid
                    s.position = x
                    s.save()
                    print "  (difffloor newfloor) moving store (#%s) %s to floor %s, position %s" % (s.id, s.name, s.floor, s.position)
        status = 'ok'
    except Exception, e:
        status = 'error'
        error_msg = "There was an error moving '%s', please try again later. " % mystore.name
        print "error when moving store: %s" % str(e)

    try:
        stores_dict = _getmall(mallid)
        ctx = {
            'stores_dict':stores_dict
            }
        mallHTML = render_to_string("mall_snippet.html", ctx, context_instance=RequestContext(request))
    except Exception, e:
        status = 'error'
        error_msg += 'Unable to retrieve mall information.'
        print "unable to generate mall after moving store: %s" % str(e)
        
    response = {
        'status':status,
        'errorMsg':error_msg,
        'mallHTML':mallHTML
        }
    return HttpResponse(json.dumps(response), mimetype="application/json")

def remove_store(request):
    uid = request.user.id
    mallid = request.POST.get("mallid")
    storeid = request.POST.get("storeid")
    success_msg = ''
    error_msg = ''
    mallHTML = ''

    # delete store image file
    try:
        si = StoreImages.objects.get(store__id=storeid)
        imgpath = "%s/%s" % (MyGlobals.STOREIMG_ROOT % { 'uid':uid }, si.path)
        output = subprocess.Popen(['rm %s'%imgpath], shell=True)
    except Exception, e:
        print "unable to delete store image file: %s" % str(e)

    try:
        if not (mallid and storeid):
            raise Exception("invalid mallid or storeid: %s; %s" % (mallid, storeid))
        store = Store.objects.get(pk=storeid, mall__id=mallid)
        store.delete()

        stores_dict = _getmall(mallid)
        ctx = {
            'stores_dict':stores_dict
            }
        mallHTML = render_to_string("mall_snippet.html", ctx, context_instance=RequestContext(request))
        
        status = 'ok'
        success_msg = "We've removed the store '%s' from your mall." % (store.name)
    except Exception, e:
        print "error removing store: %s" % str(e)
        status = 'error'
        error_msg = "We're sorry, we're unable to remove this store at this time."

    response = {
        'status':status,
        'errorMsg':error_msg,
        'successMsg':success_msg,
        'mallHTML':mallHTML
        }

    return HttpResponse(json.dumps(response), mimetype="application/json")

def login(request):
    if request.user.is_authenticated():
        mall = Mall.objects.get(user=request.user)
    	return HttpResponseRedirect("/mall/%s/"%mall.id)

    if request.method == 'POST':
    	email = request.POST.get('email', '')
    	password = request.POST.get('password', '')
    	user = auth.authenticate(username=email, password=password)
    	if user is not None:
    	    auth.login(request, user)
	    mall = Mall.objects.get(user=request.user)
            return HttpResponseRedirect("/mall/%s/"%mall.id)

    ctx_dict = {
   	'ssmedia':'/ssmedia',
    }
    return render_to_response("login.html", ctx_dict, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

def register(request):
    if request.user.is_authenticated():
    	return HttpResponseRedirect("/mall/")

    if request.method == 'POST':
	form = RegisterForm(request.POST)
	if form.is_valid():
	    user = form.create_user()
	    user.backend = settings.AUTHENTICATION_BACKENDS[0]

	    ssuser = SSUser.objects.create(user=user, bio="TBD")
	    ssuser.save()

	    mall_name = form.cleaned_data['mall_name']
	    mall = Mall.objects.create(name=mall_name, user=user)
	    mall.save()
	    auth.login(request, user)
            return HttpResponseRedirect("/mall/%s/"%mall.id)
    else:
        form = RegisterForm()

    ctx_dict = {
    	'form':form,
        'ssmedia':'/ssmedia',
    }
    return render_to_response("register.html", ctx_dict, context_instance=RequestContext(request))

def profile(request, userid):
    ctx_dict = {
        'ssmedia':'/ssmedia',
    }
    return render_to_response("profile.html", ctx_dict, context_instance=RequestContext(request))

def wishlist(request, userid):
    form = WishlistItemForm()

    wishlist_dict = _getwishlist(request)
    
    ctx_dict = {
        'ssmedia':'/ssmedia',
        'form':form,
        'all_wishlists':wishlist_dict,
    }
    return render_to_response("wishlist.html", ctx_dict, context_instance=RequestContext(request))

def _getwishlist(request):
    wishlist_dict = {}
    wishlists = Wishlist.objects.filter(user=request.user)
    for wishlist in wishlists:
        wishlistitems = WishlistItem.objects.filter(wishlist=wishlist)
        wishlistitems_list = []
        for wli in wishlistitems:
            try:
                wlimage = WishlistImages.objects.get(wishlistitem=wli)
            except:
                wlimage = None
            wishlistitems_list.append((wli, wlimage))
        wishlist_dict[wishlist] = wishlistitems_list
    return wishlist_dict
    
def add_to_wishlist(request):
    uid = request.user.id
    url = request.POST.get('url')
    tags = request.POST.get('tags')
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
        wli = WishlistItem(wishlist=wl, url=url, tags=tags, domain=domain)
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
    
def about(request):
    ctx_dict = {
        }
    return render_to_response("about.html", ctx_dict, context_instance=RequestContext(request))
