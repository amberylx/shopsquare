from django.db import models
from django.contrib.auth.models import User

class SSUser(User):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    )
    user = models.OneToOneField(User)
    bio = models.CharField(max_length=500)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')

    @property
    def mall(self):
    	return Mall.objects.get(user=self)

class Mall(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
    	return self.name

class Domain(models.Model):
    domain = models.CharField(max_length=200)

    def __unicode__(self):
        return self.domain

class Store(models.Model):
    mall = models.ForeignKey(Mall)
    domain = models.ForeignKey(Domain)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    floor = models.IntegerField()
    position = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=1000)
    is_private = models.BooleanField(default=False)
    
    def __unicode__(self):
    	return self.name
    
class StoreImages(models.Model):
    user = models.ForeignKey(User)
    store = models.ForeignKey(Store)
    path = models.CharField(max_length=1000)
    width = models.IntegerField()
    height = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.path
    
class Wishlist(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist)
    domain = models.ForeignKey(Domain)
    url = models.CharField(max_length=2000)
    tags = models.CharField(max_length=1000)
    position = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    def __unicode__(self):
        return self.url

class WishlistImages(models.Model):
    user = models.ForeignKey(User)
    wishlistitem = models.ForeignKey(WishlistItem)
    path = models.CharField(max_length=1000)
    width = models.IntegerField()
    height = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
