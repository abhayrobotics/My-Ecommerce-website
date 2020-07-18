from django.db import models

# Create your models here.
class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_heading = models.CharField(max_length=50)
    post_desc =models.CharField(max_length=5000) 
    post_author =models.CharField(max_length=50) 
    post_heading_1 =models.CharField(max_length=50) 
    post_desc_1 =models.CharField(max_length=5000) 
    post_heading_2 =models.CharField(max_length=50) 
    post_desc_2 =models.CharField(max_length=5000) 
    post_heading_3 =models.CharField(max_length=50) 
    post_desc_3 =models.CharField(max_length=5000) 
    pub_date =models.DateField()
    thumbnail= models.ImageField(upload_to='blog/images',default='')

    def __str__(self):
        return self.post_heading
