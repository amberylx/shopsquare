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
    	return Mall.objects.get(owner=self)

class Store(models.Model):
    name = models.CharField(max_length=100)
    domain = models.URLField(max_length=200)

    def __unicode__(self):
    	return self.name
    
    @property
    def floor(self):
    	return self.floorplan_set.all()[0].floor
    
    @property
    def position(self):
    	return self.floorplan_set.all()[0].position
    
class Mall(models.Model):
    name = models.CharField(max_length=50)
    stores = models.ManyToManyField(Store, through='Floorplan')
    owner = models.OneToOneField(User)
    
    def __unicode__(self):
    	return self.name

    def get_floor(self, floor_number):
        return self.floorplan_set.filter(floor=floor_number).order_by('position')
    	#return self.stores.filter(floorplan__floor=floor_number).order_by('floorplan__position')
    
class Floorplan(models.Model):
    store = models.ForeignKey(Store)
    mall = models.ForeignKey(Mall)
    floor = models.IntegerField()
    position = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
    	return "%s (%s, %s)" % (self.store.name, self.floor, self.position)

class Wishlist(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    
class WishlistItem(models.Model):
    #    store = models.ForeignKey(Store)
    wishlist = models.ForeignKey(Wishlist)
    url = models.CharField(max_length=2000)
    tags = models.CharField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
