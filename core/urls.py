from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    #Authentication
    path('api/auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('api/auth/logout/', LogoutView.as_view(next_page = "login"), name='logout'),

    #Foods
    path('api/main-foods/', views.MainFoodsView.as_view(), name='main-foods'),
    path('api/foods-details/<int:pk>', views.FoodUpdateDeleteView.as_view(), name='food-details'),
    path('api/food-create/', views.FoodCreateView.as_view(), name='food-create'),

    #Orders
    path('api/orders/', views.OrdersView.as_view(), name='orders'),
    path('api/order-myitems/', views.OrdersViewSet.as_view(), name='order-myitems'),

    #Discounts
    path('api/discounts/', views.DiscountsView.as_view(), name='discounts'),
    path('api/details/discounts/<int:pk>', views.DiscountUpdateDeleteView.as_view(), name='details-discounts' ),
    path('api/discount-create/', views.DiscountCreateView.as_view(), name='discount-create'),
]
