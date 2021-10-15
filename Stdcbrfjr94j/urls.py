from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import  static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home),
    path('profile/',views.profile),
    path('viewall/',views.viewall),
    path('checkenroll/',views.checkenroll),
    path('subscribe/',views.subscribe),
    path('viewdet/',views.viewdet),
    path('quizpage/',views.quizpage),
    path('checkanswer/',views.checkanswer),
    path('giveFeedback/',views.giveFeedback),
    path('mycor/',views.mycor),
    path('viewcourse/',views.viewcourse),
    path('checkquiz/',views.checkquiz),
    path('landingquizpage/',views.landingquizpage),
    path('performance/',views.performance),
    path('payment/',views.payment),
    path('cancel/',views.cancel),
    path('success/',views.success),
    path('viewallcat/',views.viewallcat)
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)