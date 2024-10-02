from rest_framework import serializers

from main import models

class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Project
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]