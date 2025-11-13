from django.urls import path
from apps.users.api.api import user_api_view, user_detail_api_view
from apps.users.api.views.auth_views import VerifyTokenView

urlpatterns = [
    path('', user_api_view, name='usuario_api'),
    path('<int:pk>/', user_detail_api_view, name='usuario_detail_api_view'),

    path('verify_token/', VerifyTokenView.as_view(), name='verify_token'),
]