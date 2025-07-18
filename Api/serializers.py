# Api/serializers.py

from rest_framework import serializers

from .models import TipificacionesApi,CarteraVnort,CarteraPass,RegistroContactoPass,NewEmailAvo,NewEmailSvia,NewPhoneSvia,NewEmailAvn,NewPhoneAvn,NewPhoneAvo,CarteraGlobal,BoletaAcsa,NewPhoneGlobal,NewEmailGlobal
from .models import VolverLlamar,RegistroContactoAutoriza,NewEmailPass,NewPhonePass,NewEmailCondeza,NewPhoneCondeza,CodigoRespuesta,CarteraAVO,RegistroContactoCondeza,RegistroContactoAVO,NewEmailAcsa,NewPhoneAcsa,CarteraACSA,RegistroContactoAcsa,CarteraAVO,TipificacionesReport,CarteraTotalesAVO,CarteraTotalesGlobal,RegistroContactoGlobal,CarteraGlobal,RegistroContacto,PagosAcsa,RegistroContactoVnort, Cartera,AllContacts,CarteraTotales



class TipificacionSerializerReport(serializers.ModelSerializer):
    class Meta:
        model = TipificacionesReport
        fields = '__all__'
class TipificacionSerializerApi(serializers.ModelSerializer):
    class Meta:
        model = TipificacionesApi
        fields = '__all__'

class RegistroContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContacto
        fields = '__all__'  

class AllContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllContacts
        fields = '__all__'  

class CarteraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartera
        fields = '__all__'  
        
class CarteraTotalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteraTotales
        fields = '__all__'  

class CarteraVnortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteraVnort
        fields = '__all__'  
class RegistroContactoVnortSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContactoVnort
        fields = '__all__' 

class PagosAcsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagosAcsa
        fields = '__all__'  



class RegistroContactoGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContactoGlobal
        fields = '__all__'  

class CarteraGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteraGlobal
        fields = '__all__'  
class CarteraTotalesGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteraTotalesGlobal
        fields = '__all__'  


class RegistroContactoAvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContactoAVO
        fields = '__all__'  

class CarteraAvoSerializer(serializers.ModelSerializer):
    class Meta:
        model =CarteraAVO
        fields = '__all__'  
class CarteraTotalesAvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteraTotalesAVO
        fields = '__all__'  

class CarteraAvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteraAVO
        fields = '__all__' 
        
class RegistroContactoAcsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContactoAcsa
        fields = '__all__'  
        
class RegistroContactoCondezaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContactoCondeza
        fields = '__all__'  
class CarteraAcsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteraACSA
        fields = '__all__' 

class CarteraGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteraGlobal
        fields = '__all__' 

class BoletaAcsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoletaAcsa
        fields = '__all__' 

class NewPhonoGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPhoneGlobal
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value

class NewEmailGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewEmailGlobal
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value

class NewPhonoAcsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPhoneAcsa
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value

class NewEmailAcsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewEmailAcsa
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value
    
class NewPhonoAvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPhoneAvo
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value

class NewEmailAvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewEmailAvo
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value
class NewPhonoAvnSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPhoneAvn
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value

class NewEmailAvnSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewEmailAvn
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value
    
class NewPhonoSviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPhoneSvia
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value

class NewEmailSviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewEmailSvia
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value
    

       
class NewPhonoCondezaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPhoneCondeza
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value

class NewEmailCondezaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewEmailCondeza
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value

class TipificacionCondezaSerializerReport(serializers.ModelSerializer):
    class Meta:
        model = CodigoRespuesta
        fields = '__all__'

class RegistroContactoAvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContactoAVO
        fields = '__all__'

class InsertaCallAgain(serializers.ModelSerializer):
    class Meta:
        model = VolverLlamar
        fields = '__all__'
        
class RegistroContactoPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContactoPass
        fields = '__all__'  

class CarteraPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteraPass
        fields = '__all__' 

class NewPhonoPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPhonePass
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value

class NewEmailPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewEmailPass
        fields = '__all__'

    def validate_lead_id(self, value):
        """
        Check that lead_id is an integer.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("lead_id must be an integer.")
        return value
class RegistroContactoAutorizaLLamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContactoAutoriza
        fields = '__all__' 