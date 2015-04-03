from django.conf.urls import include, url, patterns
# from django.contrib import admin

# urlpatterns = [
#     # Examples:
#     # url(r'^$', 'sentiment.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),

#     # url(r'^admin/', include(admin.site.urls)),

# ]

urlpatterns = patterns('',
    url(r'^webapp/', include('webapp.urls')),
)