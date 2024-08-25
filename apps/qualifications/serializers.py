from apps.qualifications.models import Qualification
from rest_framework import serializers

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

    def validate(self, data):
        if data['start_date'] and data['end_date']:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("End date must be after start date.")
        return data
