from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


#url urlpatterns

urlpatterns=[
    url(r'^$',views.home,name='homePage'),
    url(r'^search/', views.search_projects, name='search_projects'),
    url(r'^users/', views.user_list, name='user_list'),
    url(r'^image(\d+)',views.project,name='project'),
    url(r'^new/project$',views.new_project, name='new_project'),
    url(r'edit/profile$',views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<username>[0-9]+)$',views.individual_profile_page, name='individual_profile_page'),
    url(r'^new/image$', views.new_image, name='new_image'),
    url(r'^$', views.review_list, name='review_list'),

    url(r'review/(?P<review_id>[0-9]+)/$',views.review_details, name='review_detail'),
    url(r'project$',views.project_list, name='project_list'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)