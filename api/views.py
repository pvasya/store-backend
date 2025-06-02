from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from .models import User, Goods
from .serializers import UserSerializer, UserProfileSerializer, GoodsSerializer, UserPurchaseSerializer
from .logger import log_activity


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        user = serializer.save()
        log_activity(f'User {self.request.data["username"]} created successfully')



class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser

class GoodsListCreateView(generics.ListCreateAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = (IsAuthenticated, IsSuperUser,)

class GoodsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = (IsAuthenticated, IsSuperUser,)

class UserPurchasesView(generics.ListAPIView):
    serializer_class = UserPurchaseSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return self.request.user.purchases.all()

class AddToPurchasesView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, pk):
        try:
            goods = Goods.objects.get(pk=pk)
            user = request.user
            
            if goods in user.purchases.all():
                return Response({"message": "This item is already in your purchases."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.purchases.add(goods)
            log_activity(f'User {user.username} added item "{goods.title}" (ID: {goods.id}) to purchases')
            return Response({"message": "Item added to purchases successfully."}, status=status.HTTP_200_OK)
            

        except Goods.DoesNotExist:
            return Response({"message": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

class RemoveFromPurchasesView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, pk):
        try:
            goods = Goods.objects.get(pk=pk)
            user = request.user
            
            if goods not in user.purchases.all():
                return Response({"message": "This item is not in your purchases."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.purchases.remove(goods)
            log_activity(f'User {user.username} removed item "{goods.title}" (ID: {goods.id}) from purchases')
            return Response({"message": "Item removed from purchases successfully."}, status=status.HTTP_200_OK)
        except Goods.DoesNotExist:
            return Response({"message": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def home_view(request):
    if request.user.is_authenticated:
        return Response({
            "username": request.user.username,
            "is_blacklisted": request.user.is_blacklisted
        })
    else:
        return Response({
            "message": "Not authenticated"
        }, status=status.HTTP_401_UNAUTHORIZED)
