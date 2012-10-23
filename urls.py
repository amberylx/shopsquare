from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^ssmedia/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':settings.STATIC_MEDIA_ROOT, 'show_indexes':True}),
    ('^mall/(\d*)/$', 'mall.views.mall'),
    ('^add_store/$', 'mall.views.add_store'),
    ('^edit_floorplan/(\d*)/$', 'mall.views.edit_floorplan'),
    ('^register/$', 'mall.views.register'),
    ('^profile/$', 'mall.views.profile'),
    ('^login/$', 'mall.views.login'),
    ('^logout/$', 'mall.views.logout'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    ('', 'mall.views.landing'),
)
