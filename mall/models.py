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

    def move_store(self, store_id, newf, newp):
    	print "--> move store"
    	my_store = Store.objects.get(pk=store_id)
    	my_fp = Floorplan.objects.get(store=my_store, mall__id=self.id)
    	oldf = my_fp.floor
    	oldp = my_fp.position
    	print "current position: (%s, %s)" % (oldf, oldp)
    	
    	try:
	    if oldf == newf:
	    	print "moving within same floor"
	    	old_floor = list(self.get_floor(oldf))
	    	del old_floor[old_floor.index(my_fp)]
	    	old_floor[newp:newp] = [my_fp]

	    	for x,fp in enumerate(old_floor):
	    	    if fp.position == x:
	    	        continue
	    	    else:
	    	       fp.position = x
	    	       fp.save()
	    else:
	    	print "moving to different floor"
	    	old_floor = list(self.get_floor(oldf))
	    	del old_floor[old_floor.index(my_fp)]
	    	for x,fp in enumerate(old_floor):
	    	    if fp.position == x:
	    	        continue
	    	    else:
	    	       fp.position = x
	    	       fp.save()

                new_floor = list(self.get_floor(newf))
                if not new_floor:
                    fp = Floorplan(store=my_store, mall=self, floor=newf, position=0)
                    fp.save()
                    my_fp.delete()
                else:
                    new_floor[newp:newp] = [my_fp]

                    for x,fp in enumerate(new_floor):
                        if fp.position == x:
                            continue
                        else:
                            fp.position = x
                            fp.save()
	except Exception, e:
	    print "[ERROR] unable to move store"
	    raise Exception(e)
	else:
	    print "moved store [%s]" % my_store.name

    	return
    
class Floorplan(models.Model):
    store = models.ForeignKey(Store)
    mall = models.ForeignKey(Mall)
    floor = models.IntegerField()
    position = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
    	return "%s (%s, %s)" % (self.store.name, self.floor, self.position)
    	
    	
