from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.db import models
from utils.choice import SIZES, COLORS
from mptt.models import MPTTModel, TreeForeignKey
from user.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'shop_{}/{}'.format(instance, filename)


class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    word = models.CharField(max_length=255)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    class MPTTMeta:
        # verbose_name_plural = 'Categories'
        order_insertion_by = ['word']

    def __str__(self):
        return self.word


class Product(TimeStampedModel, ActivatorModel):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product', default=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    old_price = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    information = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=30, null=True, blank=True, choices=SIZES)
    color = models.CharField(max_length=30, null=True, blank=True, choices=COLORS)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class Contact(TimeStampedModel):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    subject = models.CharField(max_length=30)
    message = models.TextField()

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.name


class Checkout(TimeStampedModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    mobile = models.CharField(max_length=30)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip = models.IntegerField()

    class Meta:
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'

    def __str__(self):
        return self.first_name


class Newsletter(TimeStampedModel):
    email = models.EmailField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return self.email


# class Cart(TimeStampedModel):
#     cart_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     products = models.ManyToManyField(Product)
#
#     class Meta:
#         verbose_name = "Cart"
#         ordering  = ['card_id', '-']