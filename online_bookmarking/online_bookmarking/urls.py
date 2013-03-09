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

    url(r'^$','auth.views.index'),
    url(r'^signup/$','auth.signup.register'),
    url(r'^login/$','auth.signin.login'), 
    url(r'^logout/$','auth.logout.logout'),
    url(r'^change_password/$','auth.change_password.change_password'),
    url(r'^edit_profile/$','auth.edit_profile.edit_profile'),
    
    url(r'^home$', 'bookmark.bookmarks.display_bookmarks'),
    url(r'^bookmarks/$', 'bookmark.bookmarks.display_bookmarks'),
    url(r'^bookmark/$', 'bookmark.bookmarks.create_bookmark'),
    url(r'^category/$','category.views.create_category'),
    
    url(r'^tag/$','tags.views.tag_bundle'),
    url(r'^add_bookmarks_to_category/$','category.views.add_bookmarks_to_category'),
    url(r'^users/$','socialize.relationship.users'),
    url(r'^toggle/$','socialize.relationship.toggle_relationship'),
    url(r'^profile/(?P<profile_name>\w+)/$','socialize.profile.profile'),
    
    
    url(r'^tag_names/$','tags.views.retrieve_tags'),
    url(r'^tags/(?P<tag_id>\d+)','tags.views.get_bookmarks_for_tags'),
    url(r'', include('social_auth.urls')),
)
