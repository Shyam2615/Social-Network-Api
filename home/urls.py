from django.urls import path
from .views import *
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', SearchUserView.as_view(), name='search'),
    path('send-request/<int:user_id>/', SendRequest.as_view(), name='friendrequest'),
    path('friend-request/<int:request_id>/<str:action>/', FriendRequestResponseView.as_view(), name='friend_request_response'),
    path('friend-list/', FriendList.as_view(), name='friendList'),
    path('pending-friend-list/', PendingFriendRequestsView.as_view(), name='pendingList'),
]