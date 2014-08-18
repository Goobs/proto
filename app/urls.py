from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.utils.encoding import force_unicode
from django.views.generic import TemplateView


from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/', include('agora.admin.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index')
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
