from itertools import product

from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.db import models
from user.models import User
from utils.choice import SIZES, COLORS
from mptt.models import MPTTModel, TreeForeignKey


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

    def all_product(self):
        return self.product.all()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


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


class Shipping(TimeStampedModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    mobile = models.CharField(max_length=30)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip = models.IntegerField()

    class Meta:
        verbose_name = 'Billing'
        verbose_name_plural = 'Billings'

    def __str__(self):
        return self.first_name


class Newsletter(TimeStampedModel):
    email = models.EmailField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return self.email


class Review(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating')
    star = models.PositiveIntegerField(blank=True, default=0)
    text = models.TextField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1, blank=True)
    net_price = models.FloatField(max_length=255, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def save(self, *args, **kwargs):
        self.net_price = int(self.quantity) * int(self.product.price)
        super(Cart, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {} - {}".format(self.user,
                                     self.product,
                                     self.quantity)

    # @property
    # def total_item(self):
    #     count = sum(self.quantity)

    # def get_price_total(self):
    #     return sum([product.price for product in self.product.all()])


class Wishlist(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return "{} - {}".format(self.user,
                                self.product, )


# -------------------just for testing--------------------
class Test(TimeStampedModel):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)
    message = models.TextField()

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

    def __str__(self):
        return self.name
