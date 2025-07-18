from rest_framework import serializers

from Api.models import InformeGestionDiaria

class InformeGestionTodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeGestionDiaria
        fields = '__all__'