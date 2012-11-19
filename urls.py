from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('mall.views',
    url(r'^mall/(\d*)/floor/(\d*)/$', 'floor', {}, name="floor"),
    url(r'^mall/(\d*)/$', 'mall', {}, name="mall"),
    url(r'^add_to_wishlist/$', 'add_to_wishlist', {}, name='add_to_wishlist'),
    url(r'^add_store/$', 'add_store', {}, name="add_store"),
    url(r'^scrape_image/$', 'scrape_image', {}, name="scrape_image"),
    url(r'^do_crop/$', 'do_crop', {}, name="do_crop"),
    url(r'^remove_wishlistitem/$', 'remove_wishlistitem', {}, name="remove_wishlistitem"),
    url(r'^remove_store/$', 'remove_store', {}, name="remove_store"),
    url(r'^move_store/$', 'move_store', {}, name="move_store"),
    url(r'^register/$', 'register', {}, name="register"),
    url(r'^profile/(\d*)/$', 'profile', {}, name="profile"),
    url(r'^profile/(\d*)/wishlist/$', 'wishlist', {}, name="wishlist"),
    url(r'^about/$', 'about', {}, name="about"),
    url(r'^login/$', 'login', name="login"),
    url(r'^logout/$', 'logout', name="logout"),
)

urlpatterns += patterns('',
    (r'^ssmedia/store/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':settings.STATIC_STORE_IMAGE_ROOT, 'show_indexes':True}),
    (r'^ssmedia/wishlist/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':settings.STATIC_WISHLIST_IMAGE_ROOT, 'show_indexes':True}),
    (r'^ssmedia/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':settings.STATIC_MEDIA_ROOT, 'show_indexes':True}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    ('', 'mall.views.landing'),
)
