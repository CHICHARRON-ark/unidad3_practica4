from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

router = DefaultRouter()
router.register(r'users', views.UserApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', views.UserView.as_view()),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
