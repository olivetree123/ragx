from rest_framework import serializers

from main import models

class ReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Report
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]