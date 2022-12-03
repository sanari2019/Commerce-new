from ast import mod
from distutils.command import upload
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models
from django.utils.html import mark_safe
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars
from django.urls import  reverse
from django.utils import timezone
from django.conf import settings



class User(AbstractUser):
    pass
    


class Category(models.Model):
   
    item_cat = models.CharField(max_length=64,unique=True, default='select all',db_index=True)
    slug=models.SlugField(unique=True)

    class Meta:
        ordering=('-item_cat',)

    def __str__(self):
        return f"{self.item_cat}"

    def get_absolute_url(self):
        return reverse('auctions_by_category', args=[self.slug])


class AuctionType(models.Model):
    """
    ProductType Table will provide a list of the different types
    of products that are for sale.
    """

    name = models.CharField(help_text= ("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    

    def __str__(self):
        return self.name


class AuctionSpecification(models.Model):
    """
    The Product Specification Table contains product
    specifiction or features for the product types.
    """

    product_type = models.ForeignKey(AuctionType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name= ("Name"), help_text= ("Required"), max_length=255)

   

    def __str__(self):
        return self.name


#For Auction product
class Auction(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null='True')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='covers')
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=255)
    price = models.FloatField(
        help_text= ("Sample: 999.99"),
        error_messages={
            "name": {
                "max_length": ("The price must be between 0 and 999.99."),
            },
        },
        null=True
    )

    is_active = models.BooleanField(
        help_text= ("Change product visibility"),
        default=True,
    )
    
    description = models.TextField(db_index=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="wishlist", blank=True)
    buyer = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="buyer")
    current_bid = models.FloatField(blank="True", null="True")

    class Meta:
        ordering=('-creation_date',)

    def __str__(self):
        return f"{self.title}"

    # def get_absolute_url(self):
    #    return reverse('auctions:auctions_detail',args=[self.id,])


    def short_description(self):
        return truncatechars(self.description, 90)

    def image_preview(self):
        return mark_safe('<img src="{}" width="300" height="300" />'.format(self.image.url))
    image_preview.short_description = 'Image'
    image_preview.allow_tags= True

    



class AuctionSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual specification or bespoke features.
    """

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    specification = models.ForeignKey(AuctionSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        help_text= ("Product specification value (maximum of 255 words"),
        max_length=255,
    )



    def __str__(self):
        return self.value

        

    # @property
    # def image_preview(self, obj):
    #     if self.image:
    #         return mark_safe('<img src="{}" width="300" height="300" />'.format(self.image.url))
    #     return f""

class AuctionProcess(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    number_of_bids = models.IntegerField()
    time_starting = models.DateTimeField()
    time_ending = models.DateTimeField()

    def __str__(self):
        return f"{self.number_of_bids}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    time_sent = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.auction_id}"


class Bid(models.Model):

    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_price = models.FloatField(blank="True", null="True")
    listing_id = models.ForeignKey(Auction, on_delete=models.CASCADE, null="True")

    def __str__(self):
        return f"{self.listing_id}"


