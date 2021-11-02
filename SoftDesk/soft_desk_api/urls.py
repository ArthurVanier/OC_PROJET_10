from . import views
from django.urls import path, include
from rest_framework_nested import routers

from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register('projects', views.ProjectViewSet)

contributor_router = routers.NestedDefaultRouter(router, 'projects', lookup='projects')
contributor_router.register('users', views.ContributorsViewSet, basename='projects_users')


urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('create_account/', views.CreateAccount.as_view(), name="create_account"),
    path('jwt/get_token/', jwt_views.TokenObtainPairView.as_view()),
    path('jwt/refresh_token/', jwt_views.TokenRefreshView.as_view()),
    path('', include(router.urls)),
    path('', include(contributor_router.urls))
]
