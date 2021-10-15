

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import  static
from django.conf import settings
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('course/',views.course),
    path('teacher/',views.teacher),
    path('about/',views.about),
    path('pricing/',views.pricing),
    path('blog/',views.blog),
    path('contact/',views.contact),
    path('login/',views.login),
    path('Hdgeub7746h/', include('Hdgeub7746h.urls')),
    path('Stdcbrfjr94j/', include('Stdcbrfjr94j.urls')),
    path('signups/',views.signups),
    path('verify/',views.verify),
    path('signupt/',views.signupt),
    path('forget/',views.forget),
    path('changepassword/',views.changepassword),
    path('coursecat/',views.coursecat)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
