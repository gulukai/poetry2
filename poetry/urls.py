from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$/', views.getPoetry.as_view()),
    url(r'^abc/', views.basic_search),
    url(r'^author/', views.postAuthor.as_view()),
    url(r'^authorid=(.+)/', views.getAuthorById),
    url(r'^getpoetry/$', views.Optimization_Url.as_view())
]
