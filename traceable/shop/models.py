"""
Models related to Shop
Product and Order Models
"""
from django.db import models

from user.models import User


class Product(models.Model):
    """
    Product Model
    represents a product in the application
    """
    class Meta:
        db_table = 'product'

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image_url = models.CharField(max_length=255)

    def to_dict(self):
        """
        returns Product object a dictionary
        :return: dict having product object
        """
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image_url': self.image_url
        }


class Order(models.Model):
    """
    Order Model
    represents an order in the application
    """
    class Meta:
        db_table = 'order'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_on = models.DateTimeField()

    DEL = "delivered"
    RET_PEN = "return pending"
    RET = "returned"

    STATUS_CHOICES = (
        (DEL, "delivered"),
        (RET_PEN, "return pending"),
        (RET, "returned")
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DEL)

    def to_dict(self):
        """
        returns Order object a dictionary
        :return: dict having order object
        """
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'status': self.status,
            'created_on': self.created_on.strftime("%d %B %Y"),
        }


class AppliedCoupon(models.Model):
    """
    AppliedCoupon Model
    represents a mapping between coupon_code and user
    """
    class Meta:
        db_table = 'applied_coupon'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=255)
