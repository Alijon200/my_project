from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=18, unique=True)
    role = models.CharField(choices=[
        ("user", "User"),
        ("admin", "Admin")
    ], default="user")
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True, default="")



from datetime import timedelta,date
class Discount(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = date.today()


        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=10)
        super().save(*args, **kwargs)



class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    types = models.CharField(
        max_length=20,
        choices=[
            ("food", "Food"),
            ("drinks", "Drinks"),
            ("sweets", "Sweets")
        ]
    )

    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name='foods')
    image = models.ImageField(upload_to='images/', null=True, blank=True, default="")

class Orders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    location = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,
        choices=[
        ("yangi", "Yangi"),
        ("tayyorlanmoqda", "Tayyorlanmoqda"),
        ("yo'lda", "Yo'lda"),
        ("yetkazildi", "Yetkazildi")
    ])
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='orders/', null=True, blank=True, default="")



class OrderedItems(models.Model):
    food = models.ForeignKey(Food, on_delete=models.SET_NULL, null = True, blank=True)
    count = models.IntegerField()
    order =models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True, blank=True, related_name="items")
