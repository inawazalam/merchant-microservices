"""
Models related to Mechanic
Mechanic and Service Request Models
"""
from django.db import models

from user.models import User, Vehicle


class Mechanic(models.Model):
    """
    Mechanic Model
    represents a mechanic for the application
    """
    class Meta:
        db_table = 'mechanic'

    mechanic_code = models.CharField(max_length=100, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "<Mechanic: {}>".format(self.mechanic_code)

    def to_dict(self):
        """
        returns Mechanic object a dictionary
        :return: dict having mechanic object
        """
        return {
            'mechanic_code': self.mechanic_code,
            'user': self.user.to_dict()
        }


class ServiceRequest(models.Model):
    """
    Service Request Model
    represents a service request in the application
    """
    class Meta:
        db_table = 'service_request'

    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    problem_details = models.CharField(max_length=500, blank=True)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField(null=True)

    PEN = "Pending"
    FIN = "Finished"
    STATUS_CHOICES = (
        (PEN, "Pending"),
        (FIN, "Finished")
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PEN)

    def __str__(self):
        return '<ServiceRequest: {}>'.format(self.id)

    def to_dict(self):
        """
        returns Service Request object a dictionary
        :return: dict having service request object
        """
        return {
            'id': self.id,
            'mechanic': self.mechanic.to_dict(),
            'vehicle': self.vehicle.to_dict(),
            'problem_details': self.problem_details,
            'status': self.status,
            'created_on': self.created_on.strftime("%d %B, %Y, %H:%M:%S"),
        }
