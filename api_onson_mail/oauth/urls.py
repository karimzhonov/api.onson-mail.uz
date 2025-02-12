from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import SignUpView, OptView, OptVerifyView, MeView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('opt/', OptView.as_view(), name='opt'),
    path('opt-verify/', OptVerifyView.as_view(), name='opt-verify'),
    path('account/', SignUpView.as_view(), name='sign-up'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('me/', MeView.as_view())
]