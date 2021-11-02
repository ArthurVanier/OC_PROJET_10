from . import views
from django.urls import path, include
from rest_framework_nested import routers

from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register('projects', views.ProjectViewSet)

nested_project_router = routers.NestedDefaultRouter(router, 'projects', lookup='projects')
nested_project_router.register('users', views.ContributorsViewSet, basename='projects_users')
nested_project_router.register('issues', views.IssuesViewSet, basename="project_issues")

nested_project_issues_router = routers.NestedDefaultRouter(nested_project_router, 'issues', lookup='issues')
nested_project_issues_router.register('comments', views.CommentViewSet, basename='project_issues_comment')


urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('sign_up/', views.CreateAccount.as_view(), name="sign_up"),
    path('jwt/get_token/', jwt_views.TokenObtainPairView.as_view()),
    path('jwt/refresh_token/', jwt_views.TokenRefreshView.as_view()),
    path('', include(router.urls)),
    path('', include(nested_project_router.urls)),
    path('', include(nested_project_issues_router.urls))
]
