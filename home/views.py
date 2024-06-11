from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .serializers import *
from .models import Friendship
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserSignupView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSignupSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'message' : serializer.errors,
                }, status=status.HTTP_201_CREATED)
            
            serializer.save()

            return Response({
                'message' : 'Account create successfully'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'message' : 'Something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if not serializer.is_valid():
                    return Response({
                        'message' : serializer.errors,
                    }, status=status.HTTP_201_CREATED)
            
            user = authenticate(username = serializer.data['username'], password = serializer.data['password'])

            if not user:
                return Response({
                    'status' : 'False',
                    'message' : 'No user found',
                }, status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login Successfull',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        except Exception as e:
            return Response({
                'message' : 'Something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
        
class SearchUserView(APIView):
    def get(self, request):
        users = User.objects.all()

        if request.GET.get('search'):
            user = request.GET.get('search')
            users = users.filter(username__icontains = user)

        serializer = UserSerializer(users, many=True)
        
        return Response({
                'message' : 'Data Fetched Succesfully',
                'data' : serializer.data
            })
    
class SendRequest(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request, user_id):
        try:
            from_user = request.user
            to_user = User.objects.get(id = user_id)

            if from_user.friendship_requests_sent.filter(created_at__gt=timezone.now()-timezone.timedelta(minutes=1)).count() >= 3:
                return Response({"error": "You can only send 3 friend requests per minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            friendship, created = Friendship.objects.get_or_create(from_user=from_user,to_user=to_user,defaults={'status': 'pending'})

            if created:
                return Response({
                    'status' : 'Friend request sent'
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                    'status' : 'Friend request already sent'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                    'message' : 'No user found'
                }, status=status.HTTP_400_BAD_REQUEST)
        
class FriendRequestResponseView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, request_id, action):
        user = request.user

        # Debug: Ensure user is authenticated
        if not user or not user.is_authenticated:
            return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Debug: Log request information
            print(f"User: {user}, Request ID: {request_id}, Action: {action}")

            # Get the friendship request where the current user is the recipient
            friendship = Friendship.objects.get(id=request_id, to_user=user)

            if action == "accept":
                friendship.status = 'accepted'
                friendship.save()
                return Response({"success": "Friend request accepted."}, status=status.HTTP_200_OK)
            elif action == "reject":
                friendship.status = 'rejected'
                friendship.save()
                return Response({"success": "Friend request rejected."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
        except Friendship.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
        
class FriendList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            user = request.user
            friendships = Friendship.objects.filter(
                status='accepted'
            ).filter(
                Q(from_user=user) | Q(to_user=user)
            )
            
            friend_users = []
            for friendship in friendships:
                if friendship.from_user == user:
                    friend_users.append(friendship.to_user)
                else:
                    friend_users.append(friendship.from_user)
            
            serializer = UserSerializer(friend_users, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'message' : 'Something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
        
class PendingFriendRequestsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            user = request.user
            friendships = Friendship.objects.filter(
                    status='pending'
                ).filter(
                    Q(to_user=user)
                )
            pending = []
            for friendship in friendships:
                pending.append(friendship.from_user)
            serializer = UserSerializer(pending, many= True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message' : 'Something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)