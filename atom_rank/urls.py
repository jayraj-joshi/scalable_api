 
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('quiz/', include('quiz.urls')),

    path('', include('owner.urls')),
]
