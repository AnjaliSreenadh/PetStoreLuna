from django.db import models

from django.db import models
from django.contrib.auth.models import User
class Product(models.Model):
  pname=models.CharField(max_length=50)
  pcost=models.FloatField()
  pdetails=models.TextField()
  cat=models.IntegerField()
  is_active=models.BooleanField(default=True)
  pimage=models.ImageField(upload_to="image" )
  def __str__(self):
    return self.pname

class Cart(models.Model):

    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)


    def __str__(self):
        return f"Order {self.order_id} - {self.pid.pname}"


class Payment(models.Model):
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.card_holder}"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.postal_code}, {self.country}"

