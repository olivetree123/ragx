from rest_framework import serializers

from main import models

class Report2Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Report2
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]