from django.db import models

STATUS_CHOICES = ('Active' , 'Sold')
class Listing(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(choices=STATUS_CHOICES)

    category = models.ForeignKey()
    
    price = models.DecimalField()

    description = models.TextField(max_length=200)
    
    owner = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)



class ListingImage(models.Model):
    image = models.ImageField()
    
    listing = models.ForeignKey(Listing, related_name='images')