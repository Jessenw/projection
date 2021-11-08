from django.db.models import fields
from rest_framework import serializers

from .models import ProjectPreview

class ProjectPreviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectPreview
        fields = ('title', 'link', 'author', 'replied_count', 'view_count', 'last_post_at')