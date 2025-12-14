from django.shortcuts import render
from rest_framework import pagination, permissions
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import  DjangoFilterBackend
from . import serializer
from . import models





@extend_schema(
    tags=["Auth"],
    description="Agar ro'yhatdan o'tgan bo'lsangiz, login qila olasiz",
    summary="Login qilish faqat ro'yxatdan o'tgandan keyin",
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializer.CustomTokenObtainPairViewSerializer



@extend_schema(
    tags=["Auth"],
    description="Siz accessTokeni RefreshToken yordamida yangilay olasiz",
    summary="AccesTokeni yangilash uchun"
    )
class CustomTokenRefreshView(TokenRefreshView):
    pass



@extend_schema(
    tags=["Auth"],
    description="Ro'yhatdan o'tish",
    summary="Ro'yhatdan o'tish",
)
class SignUpView(CreateAPIView):
    serializer_class = serializer.SignupSerializer
    queryset = models.CustomUser.objects.all()



class FoodPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class MainFoodsView(ListAPIView):
    queryset = models.Food.objects.all()
    serializer_class = serializer.FoodSerializer
    pagination_class = FoodPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['types']

    @extend_schema(
        tags=["Foods"],
        summary="Taomlar ro‘yxati, hamma uchun",
        description="Barcha foydalanuvchilar taomlarni ko‘ra oladi"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)





class FoodUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.FoodSerializer
    queryset = models.Food.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


    @extend_schema(
        tags=["Foods"],
        summary="Taomni yangilash, admin uchun",
        description="Faqat admin taomni yangilay oladi"
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=["Foods"],
        summary="Taomni o'chirish, admin uchun",
        description="Faqat admin taomni o'chira oladi"
    )
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        tags=["Foods"],
        summary="Taomni qisman yangilash, admin uchun",
        description="Faqat admin taomni yangilay oladi"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["Foods"],
        summary="Bitta taomni tanlab olish, admin uchun",
        description="Faqat admin taomni bitta taomni oladi"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)




class FoodCreateView(CreateAPIView):
    serializer_class = serializer.FoodSerializer
    queryset = models.Food.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(
        tags=["Foods"],
        summary="Taom qo'shish, admin uchun",
        description="Faqat admin taomni qo'sha oladi"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)





class OrdersView(CreateAPIView):
    serializer_class = serializer.OrdersSerializer
    queryset = models.Orders.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Orders"],
        summary="Buyurtma berish, hamma uchun",
        description="Hamma buyurtma bera oladi"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OrdersViewSet(ListAPIView):
    serializer_class = serializer.OrdersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Orders.objects.filter(user=self.request.user)

    @extend_schema(
        tags=["Orders"],
        summary="Mening buyurtmalar tarixim",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)




class DiscountsView(ListAPIView):
    queryset = models.Discount.objects.all()
    serializer_class = serializer.DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Discount"],
        summary="Chegirmalarni k'rish, hamma uchun",
        description="Chegirmalarni hamma ko'ra oladi"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class DiscountUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = models.Discount.objects.all()
    serializer_class = serializer.DiscountSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    @extend_schema(
        summary="Faqat bitta chegirmani ko‘rish, admin uchun",
        description="Faqat admin ko‘ra oladi",
        tags=["Discount"]
    )
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary="Chegirmani yangilash, admin uchun",
        description="Faqat admin yangilay oladi",
        tags=["Discount"]
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @extend_schema(
        tags=["Discount"],
        summary="Chegirmani qisman yangilash, admin uchun",
        description="Faqat admin yangilay oladi",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


    @extend_schema(
        summary="Chegirmani o‘chirish, admin uchun",
        description="Faqat admin o‘chira oladi",
        tags=["Discount"]
    )
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



class DiscountCreateView(CreateAPIView):
    serializer_class = serializer.DiscountSerializer
    queryset = models.Discount.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(
        tags=["Discount"],
        summary="Yangi chegirma yaratish, admin uchun",
        description="Faqat admin yangi chegirma yarata oladi",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)





