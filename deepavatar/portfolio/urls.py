from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
	path('', views.IndexView.as_view(), name="home"),
	path('contact/', views.ContactView.as_view(), name="contact"),
	path('projects/', views.ProjectsView.as_view(), name="projects"),
	path('projects/<slug:slug>', views.ProjectsDetailView.as_view(), name="projects"),
    path('get_avatar_response/', views.get_avatar_response, name='get_avatar_response'),
    path('start_avatar_chat_to_user/', views.start_avatar_chat_to_user, name='start_avatar_chat_to_user'),
    path('check_for_new_posted_video/', views.check_for_new_posted_video, name='check_for_new_posted_video'),
    path('update_avatar_feed/<str:video_path>/', views.update_avatar_feed, name='update_avatar_feed')
]