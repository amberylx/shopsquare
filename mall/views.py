from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import Store, Mall, Floorplan, SSUser
from forms import RegisterForm, AddStoreForm, EditFloorplanForm

def landing(request):
    ctx_dict = {
    	'request':request,
    	'ssmedia':'/ssmedia',
    }
    return render_to_response('landing.html', RequestContext(request, ctx_dict))

@login_required
def mall(request, mall_id):
    form = AddStoreForm()
    mall = Mall.objects.get(pk=mall_id)

    all_stores = mall.stores.all().order_by('floorplan__floor', 'floorplan__position') if mall else []
    stores_dict = {}
    for store in all_stores:
        try:
            stores_dict[store.floor].append(store)
        except:
            stores_dict[store.floor] = [store]

    ctx_dict = {
    	'form':form,
    	'mall':mall,
    	'stores_dict':stores_dict,
    	'request':request,
    	'ssmedia':'/ssmedia',
    }
    return render_to_response('mall.html', RequestContext(request, ctx_dict))

def add_store(request):
    if request.method == 'POST':
	form = AddStoreForm(request.POST)
	if form.is_valid():
	    data = form.cleaned_data
	    name = data['name']
	    domain = data['domain']
	    new_store = Store.objects.create(name=name, domain=domain)
	    mall = Mall.objects.get(owner=request.user)
	    floor = 0
	    pos_count = len(mall.get_floor(floor))
	    floorplan = Floorplan(store=new_store, mall=mall, floor=floor, position=pos_count)
	    floorplan.save()
            return HttpResponseRedirect("/mall/%s/"%mall.id)
    else:
        form = AddStoreForm()

    ctx_dict = {
    	'form':form,
    	'request':request,
   	'ssmedia':'/ssmedia',
    }
    return render_to_response("mall.html", RequestContext(request, ctx_dict))

def edit_floorplan(request, mall_id):
    mall = Mall.objects.get(pk=mall_id)
    stores = mall.stores.all().order_by('floorplan__position') if mall else []
    
    if request.method == 'POST':
    	form = EditFloorplanForm(request.POST)
    	if form.is_valid():
    	    data = form.cleaned_data
    	    sid = data['store_id']
    	    new_floor = data['new_floor']
    	    new_position = data['new_position']
    	    mall.move_store(sid, new_floor, new_position)
    	    return HttpResponseRedirect("/edit_floorplan/%s/"%mall_id)
    else:
        form = EditFloorplanForm()

    ctx_dict = {
    	'form':form,
    	'mall':mall,
    	'stores':stores,
    	'request':request,
   	'ssmedia':'/ssmedia',
    }
    return render_to_response("edit_floorplan.html", RequestContext(request, ctx_dict))

def login(request):
    if request.user.is_authenticated():
        mall = Mall.objects.get(owner=request.user)
    	return HttpResponseRedirect("/mall/%s/"%mall.id)

    if request.method == 'POST':
    	email = request.POST.get('email', '')
    	password = request.POST.get('password', '')
    	user = auth.authenticate(username=email, password=password)
    	if user is not None:
    	    auth.login(request, user)
	    mall = Mall.objects.get(owner=request.user)
            return HttpResponseRedirect("/mall/%s/"%mall.id)

    ctx_dict = {
   	'ssmedia':'/ssmedia',
    }
    return render_to_response("login.html", RequestContext(request, ctx_dict))

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
	    mall = Mall.objects.create(name=mall_name, owner=user)
	    mall.save()
	    auth.login(request, user)
            return HttpResponseRedirect("/mall/%s/"%mall.id)
    else:
        form = RegisterForm()

    ctx_dict = {
    	'form':form,
   	'ssmedia':'/ssmedia',
    }
    return render_to_response("register.html", RequestContext(request, ctx_dict))

def profile(request):
    ctx_dict = {
    	'request':request,
   	'ssmedia':'/ssmedia',
    }
    return render_to_response("profile.html", RequestContext(request, ctx_dict))
