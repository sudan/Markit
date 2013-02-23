from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'online_bookmarking.views.home', name='home'),
    # url(r'^online_bookmarking/', include('online_bookmarking.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^bookmark/$', 'bookmark.bookmarks.create_bookmark'),
    url(r'^signup/$','auth.signup.register'),
    url(r'^login/$','auth.signin.login'),   
    url(r'^logout/$','auth.logout.logout'),
    #url(r'^login_status/$','auth.login_status.is_logged_in'),
    # url(r'^$', 'auth.views.login'),
    url(r'^home$', 'bookmark.bookmarks.display_bookmarks'),
    url(r'^tags/$','tags.views.tag_bundle'),
    url(r'^category/$','category.views.create_category'),
    url(r'^add_bookmarks_to_category/$','category.views.add_bookmarks_to_category'),
    url(r'', include('social_auth.urls')),
)
