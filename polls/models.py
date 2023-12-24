from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.urls import reverse
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, phone, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, default='N/A')
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return self.username

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - Product {self.product_id} - Quantity {self.quantity}"
    
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    create_by = models.CharField(max_length=255, default='admin')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    intro = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    suplier = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True)
    release_date = models.DateField()
    language = models.CharField(max_length=255)
    weight = models.IntegerField()
    size = models.CharField(max_length=255)
    page = models.IntegerField()
    book_quality = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    price = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
    
    def get_absolute_url(self):
        return reverse('polls:product_detail', args=[self.slug])

    def __str__(self):
        return self.title