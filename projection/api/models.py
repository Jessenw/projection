from django.db import models
from django.db.models.base import Model


class ProjectPreview(models.Model):
    title = models.CharField(max_length=60)
    link = models.CharField(max_length=60)
    author = models.CharField(max_length=60) # This will need to be a list of authors
    replied_count = models.IntegerField()
    view_count = models.IntegerField()
    last_post_at = models.DateField()

    def __str__(self):
        return self.title
