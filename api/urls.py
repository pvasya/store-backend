from django.urls import path
from .views import (
    GoodsListCreateView,
    UserPurchasesView,
    AddToPurchasesView,
    RemoveFromPurchasesView,
)

urlpatterns = [
    path('goods/', GoodsListCreateView.as_view(), name='goods-list-create'),
    path('purchases/', UserPurchasesView.as_view(), name='user-purchases'),
    path('purchases/add/<int:pk>/', AddToPurchasesView.as_view(), name='add-to-purchases'),
    path('purchases/remove/<int:pk>/', RemoveFromPurchasesView.as_view(), name='remove-from-purchases'),
]
