from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.utils.encoding import force_unicode


from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^robokassa/', include('robokassa.urls')),
)

for app in settings.APPS:
    try:
        urlpatterns += (url(r'^', include(app + '.urls')),)
    except Exception, e:
        if str(e) == 'No module named urls':
            print 'Warning: Unable to include urls for %s!' % app
        else:
            raise

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=force_unicode(settings.MEDIA_ROOT))
    urlpatterns += static(settings.STATIC_URL, document_root=force_unicode(settings.STATIC_ROOT))

# urlpatterns += (
#     url(r'^', include('app.cms.urls')),
# )
