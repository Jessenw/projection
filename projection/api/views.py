from django.shortcuts import render
from rest_framework import serializers, viewsets

from .serializers import ProjectPreviewSerializer
from .models import ProjectPreview

class ProjectPreviewViewSet(viewsets.ModelViewSet):
    queryset = ProjectPreview.objects.all().order_by('last_post_at')
    serializer_class = ProjectPreviewSerializer
