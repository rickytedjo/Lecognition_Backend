from django.db import models
from datetime import datetime
import os

def image_path(instance, filename):
    filename = datetime.now().strftime('%Y%m%d') + ' - ' + filename

    os.path.join('storage/image/',filename)

    return filename

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

class Scan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.PositiveBigIntegerField()
    img = models.ImageField(upload_to='storage/image')
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    desc = models.TextField(blank=True)

    class Meta:
        db_table = 'Scan'

    def save(self, *args, **kwargs):
        # Check if the image is being uploaded
        if self.img:
            # Generate a new filename
            new_filename = datetime.now().strftime('%Y%m%d') + ' - ' + self.img.name
            self.img.name = new_filename
        # Call the original save method
        super().save(*args, **kwargs)
    

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    date = models.PositiveBigIntegerField()

    class Meta:
        db_table = 'Bookmark'
