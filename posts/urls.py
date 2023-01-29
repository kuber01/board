from django.urls import path
from .views import PostList, PostCreate, PostUpdate, PostRespond, ResponseList, accept_response, \
    delete_response

urlpatterns = [
    path('', PostList.as_view(), name="home"),
    path('new', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/response', PostRespond.as_view(), name='respond'),
    path('responses/', ResponseList.as_view(), name='response_list'),
    path('responses/<int:pk>/accept', accept_response, name='accept_response'),
    path('responses/<int:pk>/delete', delete_response, name='delete_response')
]
