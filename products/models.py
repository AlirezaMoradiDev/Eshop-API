from django.db import models
from django.db.models import Count

from user.models import MyUser
from django.utils.text import slugify
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save()


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save()


class ProductImage(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/', null=True, blank=True)


class Order(models.Model):

    payment_method_choice = [
        ('Paypal', 'PayPal'),
        ('Credit Card', 'Credit Card')
    ]

    status_choice = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]

    order_number = models.CharField(max_length=8, unique=True, null=True, blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=status_choice)
    payment_method = models.CharField(max_length=20, choices=payment_method_choice)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.order_number

    def save(self,*args, **kwargs):
        if not self.order_number:
            last = Order.objects.all().order_by('-id').first()
            if last and last.order_number.isdigit():
                self.order_number = str(int(last.order_number) + 1)
            else:
                self.order_number = '1000'
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} Cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.cart} Item'

class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def calculate_subtotal(self):
        self.subtotal = self.quantity * self.price_at_purchase
