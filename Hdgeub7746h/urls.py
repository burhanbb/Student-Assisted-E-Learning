from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import  static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home),
    path('profile/',views.profile),
    path('MyCourse/',views.mycourse),
    path('addcourse/',views.addcourse),
    path('editcourse/',views.editcourse),
    path('blog/',views.blogs),
    path('addblog/',views.addblog),
    path('editblog/',views.editblog),
    path('feedback/',views.feedback),
    path('comments/',views.comments),
    path('coursepage/',views.coursepage),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)