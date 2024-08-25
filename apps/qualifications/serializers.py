from apps.qualifications.models import Qualification
from rest_framework import serializers

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError("End date must be after start date.")
        return data
