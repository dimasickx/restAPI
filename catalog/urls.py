from django.urls import path
from . import views


urlpatterns = [
    path('pets/', views.pet_list, name='pets'),
    path(r'pets/<uuid:pk>', views.pet_detail, name='pet-detail'),
    path(r'pets/<uuid:pk>/photo', views.upload_photo, name='upload-photo'),
]
