from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser, Food, Orders, OrderedItems, Discount



class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'phone')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Telefon raqam faqat raqamlardan iborat bo‘lishi kerak.")
        return value




class CustomTokenObtainPairViewSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['accessToken'] = data.pop('access')
        data['refreshToken'] = data.pop('refresh')
        data['user'] = {
            'user_id': self.user.id,
            'username': self.user.username,
            'phone': self.user.phone,
            'role': self.user.role,
            'avatar_url': self.user.avatar.url if self.user.avatar else ""
        }
        return data


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ("id", "name", "amount", "start_date", "end_date")
        extra_kwargs = {
            "end_date": {"read_only": True},
            "start_date": {"read_only": True},
            "id": {"read_only": True},
        }


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'price', 'types', 'image', 'discount')



class OrderItemsSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderedItems
        fields = ('food', 'count', "total_price")

    def get_total_price(self, obj):
        if obj.food and obj.count:
            return obj.food.price * obj.count
        return 0




class OrdersSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True, format="%d-%m-%Y") 

    class Meta:
        model = Orders
        fields = ('id', 'location', 'status', 'items', 'discount', 'total_price', "created_at")

    def get_total_price(self, obj):
        total = sum(item.food.price * item.count for item in obj.items.all() if item.food)
        if obj.discount and total >= 200_000:
            total -= obj.discount.amount
        return total

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        discount = validated_data.pop('discount', None)
        location = validated_data.pop('location')
        status = validated_data.pop('status', 'yangi')

        from django.db import transaction
        with transaction.atomic():

            order = Orders.objects.create(
                user=self.context["request"].user,
                location=location,
                status=status,
            )

            total = 0
            for item in items_data:
                OrderedItems.objects.create(
                    order=order,
                    food=item['food'],
                    count=item['count']
                )
                total += item['food'].price * item['count']

            if total < 200_000:
                raise serializers.ValidationError(
                    "Siz hali 200_000 so‘mlik savdo qilmagansiz"
                )

            if discount and total >= 200_000:
                order.discount = discount

            order.save()

        return order






