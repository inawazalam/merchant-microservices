"""
Models related to User
These tables are created by user microservices
So fake migrations are performed on these models
"""
from django.db import models


class User(models.Model):
    """
    User Model
    represents an user for the application
    """
    class Meta:
        db_table = 'user_login'

    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField()
    email = models.CharField(max_length=255, unique=True)
    jwt_token = models.CharField(max_length=500, unique=True, null=True)
    number = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255)

    MECH = 2
    USER = 0
    ROLE_CHOICES = (
        (MECH, 1),
        (USER, 0)
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=USER)

    def __str__(self):
        return "<User: {}>".format(self.email)

    def to_dict(self):
        """
        returns User object a dictionary
        :return: dict having user object
        """
        return {
            'email': self.email,
            'number': self.number
        }


class UserDetails(models.Model):
    """
    UserDetails Model
    stores additional details for the user
    """
    class Meta:
        db_table = 'user_details'

    available_credit = models.FloatField()
    name = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Vehicle(models.Model):
    """
    Vehicle Model
    represents a vehicle in the application
    """
    class Meta:
        db_table = 'vehicle_details'

    pincode = models.CharField(max_length=255, null=True)
    vin = models.CharField(max_length=255)
    year = models.BigIntegerField(null=True)
    vehicle_modelid = models.BigIntegerField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    location_id = models.BigIntegerField(null=True)

    def to_dict(self):
        """
        returns UserDetails object a dictionary
        :return: dict having all extra details of the user
        """
        return {
            'vin': self.vin,
            'owner': self.owner.to_dict()
        }
