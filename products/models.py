from turtle import mode
from django.db import models

from django.contrib import admin
from customer.models import Customer

# Create your models here.
class Category(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

class NewSubCategory(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    par_category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name





class Product(models.Model):
    Categorie = (
        ("New Arrivals", "New Arrivals"),
        ("Pets", "Pets"),
        ("Pet Accessories", "Pet Accessories"),
        ("Pet food", "Pet food"),
        ("Aquariums", "Aquariums")
    )
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    vote_total=models.IntegerField(default=0, null=True, blank=True)
    vote_ratio=models.IntegerField(default=0, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    choice = models.CharField(
        max_length=300, null=True, blank=True, choices=Categorie)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null= True, blank=True )
    subcategory = models.ForeignKey(NewSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    buy_count = models.IntegerField(default=0, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    dimensions = models.CharField(max_length=100, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
 
 

    def __str__(self):
        return self.title

    @property
    def imageurl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def getStock(self):
        if self.stock_quantity is None:
            self.in_stock = False
            return self.in_stock
        else:
            self.in_stock = True
            return self.in_stock

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes/ totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()
        
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    #for customer commenting on product
    owner=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)

    #binds customer profile and product
    class Meta:
        unique_together=[['owner', 'product']]

    def __str__(self):
        return self.value


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'category', 'buy_count')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name',)

class NewSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'par_category')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(NewSubCategory, NewSubCategoryAdmin)