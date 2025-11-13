from django.contrib import admin
from django.urls import path, include

from apps.users.api.views.auth_views import Login, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/', include('apps.users.api.urls')),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout')
]
