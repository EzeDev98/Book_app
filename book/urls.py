from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>', views.story_page, name="story_page"),
    path('<int:id>', views.search_page, name="search_page"),
    path('form', views.form, name='form'),
    path('about', views.about, name='about'),
    path('landing_page', views.landing_page, name='landing_page'),
    path('service', views.service, name='service'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('premium', views.premium, name='premium'),
    path('projects', views.projects, name='projects'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('sponsors', views.sponsors, name='sponsors'),
    path('mentorship', views.mentorship, name='mentorship'),
    path('logout', views.logout, name='logout'),
]
