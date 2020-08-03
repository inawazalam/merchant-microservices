"""
Configuration for traceable application
"""
from django.apps import AppConfig
import mimetypes
import bcrypt
from django.utils import timezone
from django.db import models
from utils import messages


class TraceableConfig(AppConfig):
    """
    Stores all meta data of traceable application
    """
    name = 'traceable'

    def ready(self):
        """
        Pre-populate mechanic model
        :return: None
        """
        from user.models import User, UserDetails
        from traceable.mechanic.models import Mechanic
        from traceable.shop.models import Product
        try:
            product_details_all = [
                {
                    'name': 'Seat',
                    'price': 10,
                    'image_url': 'https://4.imimg.com/data4/NI/WE/MY-19393581/ciaz-car-seat-cover-500x500.jpg'
                },
                {
                    'name': 'Wheel',
                    'price': 10,
                    'image_url': 'https://i.dlpng.com/static/png/6446943_preview.png'
                }
            ]
            for product_details in product_details_all:
                if product_details['name'] in map(lambda a: a.name, Product.objects.all()):
                    print('Product, {} already exists'.format(product_details['name']))
                    continue
                product = Product(
                    name=product_details['name'],
                    price=float(product_details['price']),
                    image_url=product_details['image_url']
                )
                product.save()
                print(messages.PRODUCT_SAVED.format(product.id))
            mechanic_details_all = [
                {
                    'name': 'Jhon',
                    'email': 'jhon@gmail.com',
                    'number': '',
                    'password': 'Admin1@#',
                    'mechanic_code': 'TRAC_JHN'
                },
                {
                    'name': 'James',
                    'email': 'james@gmail.com',
                    'number': '',
                    'password': 'Admin1@#',
                    'mechanic_code': 'TRAC_JME'
                },
            ]
            for mechanic_details in mechanic_details_all:
                if mechanic_details['email'] in map(lambda a: a.email, User.objects.all()):
                    print('Mechanic email, {} already exists'.format(mechanic_details['email']))
                    continue
                if mechanic_details['mechanic_code'] in map(
                        lambda a: a.mechanic_code,
                        Mechanic.objects.all()
                ):
                    print('Mechanic code, {} already exists'.format(mechanic_details['mechanic_code']))
                    continue
                try:
                    user_id = User.objects.aggregate(models.Max('id'))['id__max'] + 1
                except TypeError:
                    user_id = 1
                user = User.objects.create(
                    id=user_id,
                    email=mechanic_details['email'],
                    number=mechanic_details['number'],
                    password=bcrypt.hashpw(
                        mechanic_details['password'].encode('utf-8'),
                        bcrypt.gensalt()
                    ).decode(),
                    role=User.MECH,
                    created_on=timezone.now()
                )
                Mechanic.objects.create(
                    mechanic_code=mechanic_details['mechanic_code'],
                    user=user
                )
                try:
                    user_details_id = UserDetails.objects.aggregate(models.Max('id'))['id__max'] + 1
                except TypeError:
                    user_details_id = 1
                UserDetails.objects.create(
                    id=user_details_id,
                    available_credit=0,
                    name=mechanic_details['name'],
                    status='ACTIVE',
                    user=user
                )
                print(messages.MEC_CREATED.format(user.email))
        except Exception as error:
            print(repr(error))

