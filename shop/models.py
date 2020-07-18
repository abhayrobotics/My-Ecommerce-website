from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name= models.CharField(max_length=50)
    category= models.CharField(max_length=50, default="")
    subcategory= models.CharField(max_length=50, default="")
    price =models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date =models.DateField()
    image= models.ImageField(upload_to ="shop/images",default="")

    def __str__(self):
        return self.product_name

# contact us form database
class Contact(models.Model):
    msg_id = models.AutoField(primary_key= True)
    name= models.CharField(max_length=50)
    email= models.CharField(max_length=50, default="")
    purpose= models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=300)

    

    def __str__(self):
        return self.name

# All order database

class Order123(models.Model):
    order_id = models.AutoField(primary_key= True)
    items_json = models.CharField(max_length= 5000)
    amount =models.IntegerField(default=0)
    name = models.CharField(max_length= 500)
    email = models.CharField(max_length= 500)
    address = models.CharField(max_length= 500)
    phone = models.CharField(max_length=12,default='')
    city = models.CharField(max_length= 500)
    state = models.CharField(max_length= 500)
    zipcode = models.CharField(max_length= 8)

    def __str__(self):
        return "ORD" + str(self.order_id)
 
#  order status - track

class Orderupdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=50,default='')
    update_desc = models.CharField(max_length=500)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:18]+ "..."