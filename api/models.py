from django.db import models
from datetime import datetime
import os

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    avatar = models.IntegerField(default = 1)

    class Meta:
        db_table = 'User'

class Disease(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True)

    class Meta:
        db_table = 'Disease' 

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    date = models.PositiveBigIntegerField()

    class Meta:
        db_table = 'Bookmark'

class Tree(models.Model):
    desc = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    longitude = models.FloatField(default=0) # X
    latitude = models.FloatField(default=0) # Y
    image = models.ImageField(upload_to='storage/trees', null= True)
    last_predicted_disease = models.ForeignKey('Scan', on_delete=models.SET_NULL, null=True,related_name='last_predicted_trees')

    class Meta:
        db_table = 'Tree'

    def save(self, *args, **kwargs):
        # Check if the image is being uploaded
        if self.image:
            # Generate a new filename
            new_filename = str(int(round(datetime.now().timestamp()))) + ' - ' + self.image.name
            self.image.name = new_filename
        # Call the original save method
        super().save(*args, **kwargs)

class Scan(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE,related_name='scans')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.PositiveBigIntegerField()
    img = models.ImageField(upload_to='storage/scans')
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    desc = models.TextField(blank=True)

    class Meta:
        db_table = 'Scan'

    def save(self, *args, **kwargs):
        # Check if the image is being uploaded
        if self.img:
            # Generate a new filename
            new_filename = str(int(round(datetime.now().timestamp()))) + ' - ' + self.img.name
            self.img.name = new_filename
        # Call the original save method
        super().save(*args, **kwargs)

        self.tree.last_predicted_disease = self
        self.tree.save()
   