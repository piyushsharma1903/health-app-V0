from rest_framework import serializers
from .models import MedicalReport

#class MedicalReportSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = MedicalReport
        #fields = '__all__'
# # This serializer will automatically include all fields from the MedicalReport model

class MedicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalReport
        fields = ['id', 'report_date', 'report_type', 'ai_summary', 'original_file']

