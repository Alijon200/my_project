from django.contrib import admin


from . import models
# Register your models here.

@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fields = ["username", "phone", "role"]
    list_display = ["username", "phone", "role"]


@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    fields = ["name", "price", "image", "types"]
    list_display = ["name"]


@admin.register(models.Discount)
class DiscountAdmin(admin.ModelAdmin):
    fields = ["name", "amount"]
    list_display = ["name", "amount"]


@admin.register(models.Orders)
class OrdersAdmin(admin.ModelAdmin):
    fields = ["user", "location", "total_price", "discount", "status"]
    list_display = ["location", "status"]


@admin.register(models.OrderedItems)
class OrderItemAdmin(admin.ModelAdmin):
    fields = ["food", "count", "order"]
    list_display = ["food", "count"]

