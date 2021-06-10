import uuid
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
import os


# Create your models here.


class Pet(models.Model):
    choice = [('cat', 'cat'), ('dog', 'dog')]

    id = models.UUIDField(primary_key=True, help_text='PK id', default=uuid.uuid4, editable=False)
    name = models.CharField(help_text='Name', max_length=40)
    age = models.IntegerField(help_text='Age of pets')
    type = models.CharField(max_length=3, choices=choice, default='Pet')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created time')

    def get_absolute_url(self):
        return reverse('pet-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.type}: name {self.name}, {self.age} years old"


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, help_text='PK id', default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, to_field='id', related_name='photo')
    photo = models.ImageField(upload_to='PetsPhoto', default='default.jpg')

    @property
    def get_image_url(self):
        return f'{{\n\r\"id\": {self.id}\n\r\"url\": {self.photo.url}\n\r}}'


@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)
