from django.db import models

# Create your models here. 

# Api/models.py


#svia

class AllContacts(models.Model):
    lead_id = models.IntegerField(null=True, blank=True)
    rut = models.CharField(null=True, max_length=20)  # Usando 'rut' como clave primaria
    ruteje = models.CharField(max_length=11, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    glosa = models.CharField(max_length=255, null=True, blank=True)
    feccomp = models.DateField(null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)
    respuesta = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=2, null=True, blank=True)
    uniqueid = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'All_Contacts' # Especifica el nombre exacto de la tabla en la base de datos
        app_label = 'svia'


class RegistroContacto(models.Model):
    lead_id = models.IntegerField(null=True,blank=True)
    idrespuesta = models.IntegerField(max_length=11,null=True,blank=True)
    rut = models.CharField(max_length=11, blank=True,null=True)
    ruteje = models.CharField(max_length=12,blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True,null=True)
    glosa = models.CharField(max_length=255,blank=True, null=True)
    numdoc = models.IntegerField(null=True,blank=True)
    monto = models.IntegerField(null=True,blank=True)
    feccomp = models.DateField(null=True,blank=True)
    estcomp = models.CharField(max_length=20,blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  
    tipocomp = models.IntegerField(null=True,blank=True)
    abono = models.CharField(max_length=255,blank=True ,null=True)
    uniqueid = models.CharField(max_length=20,blank=True, null=True)
    modo = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Registro_Contacto'  
        app_label = 'svia'


class Cartera(models.Model):
    ctacto = models.CharField(max_length=16, null=True, blank=True)
    rut = models.CharField(max_length=10, null=True, blank=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    folio = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fec_emi = models.DateField(null=True, blank=True)
    fec_vcto = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    comuna = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    celular = models.BigIntegerField(null=True, blank=True)
    fono_2 = models.BigIntegerField(null=True, blank=True)
    fono_3 = models.BigIntegerField(null=True, blank=True)
    fono_4 = models.BigIntegerField(null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    tipo_doc = models.CharField(max_length=2, null=True, blank=True)
    dias_mora = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    tramo_mora = models.CharField(max_length=100, null=True, blank=True)
    tipo_convenio = models.CharField(max_length=10, null=True, blank=True)
    cantidad_folios = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    fecha_asignacion = models.DateField(null=True, blank=True)
    empresa = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    rutdv = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'Cartera'
        app_label = 'svia'


class CarteraTotales(models.Model):
    rut = models.CharField(max_length=11, null=True, blank=True)
    CtaCto = models.CharField(max_length=16, null=True, blank=True)
    boletas = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vence = models.DateField(null=True, blank=True)
    vence1 = models.DateField(null=True, blank=True)
    rutdv = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'Cartera_Totales'
        app_label = 'svia'

#vistas

class InformeGestionDiaria(models.Model):
    tipo = models.CharField(max_length=255)
    respuesta = models.CharField(max_length=255)
    fecha_gestion = models.DateTimeField()
    agente = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fec_compromiso = models.DateField()
    glosa = models.TextField()

    class Meta:
        managed = False  # Esto indica que Django no debería intentar crear esta tabla
        db_table = 'vw_informe_gestion_diaria'
        app_label = 'svia'
#api


class NewPhoneSvia(models.Model):
    lead_id = models.IntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  
    class Meta:
        managed = False 
        db_table = 'New_Phone'
        app_label = 'svia'

class NewEmailSvia(models.Model):
    lead_id = models.IntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  

    class Meta:
        managed = False 
        db_table = 'New_Email'
        app_label = 'svia'

#vnort


class CarteraVnort(models.Model):
    id = models.BigAutoField(primary_key=True)  # IDENTITY
    ctacto = models.CharField(max_length=255, null=True, blank=True)
    bp = models.CharField(max_length=255, null=True, blank=True)
    rut = models.CharField(max_length=50, null=True, blank=True)
    razon_social = models.CharField(max_length=255, null=True, blank=True)
    folio = models.CharField(max_length=255, null=True, blank=True)
    deuda = models.CharField(max_length=255, null=True, blank=True)
    fec_vcto = models.CharField(max_length=255, null=True, blank=True)
    fec_emi = models.CharField(max_length=255, null=True, blank=True)
    dirección = models.CharField(max_length=200, null=True, blank=True)  # Note the field name
    complemento = models.CharField(max_length=200, null=True, blank=True)
    comuna = models.CharField(max_length=50, null=True, blank=True)
    ciudad = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    fono_1 = models.CharField(max_length=255, null=True, blank=True)
    fono_2 = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    tipo_doc = models.CharField(max_length=255, null=True, blank=True)
    dias_mora = models.CharField(max_length=255, null=True, blank=True)
    proveedor = models.CharField(max_length=50, null=True, blank=True)
    rangodeuda = models.CharField(max_length=255, null=True, blank=True)
    matrizansoff = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Cartera'  # Matches the SQL table name exactly
        app_label = 'vnorte'
        

class CarteraTotalesVnort(models.Model):
    rut = models.CharField(max_length=11, null=True)
    tramo_deuda = models.CharField(max_length=50, null=True)
    boletas = models.IntegerField(null=True)
    monto = models.IntegerField(null=True)
    dias = models.IntegerField(null=True)
    vence = models.DateField(null=True)
    vence1 = models.DateField(null=True)
    tipo = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Cartera_Totales'  # Especifica el nombre completo de la tabla si es necesario
        app_label = 'vnorte' 

class RegistroContactoVnort(models.Model):
    lead_id = models.IntegerField()
    idrespuesta = models.CharField(max_length=3,blank=True, null=True)
    rut = models.CharField(max_length=11, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    glosa = models.TextField(null=True ,blank=True,)
    numdoc = models.IntegerField(null=True ,blank=True,)
    monto = models.IntegerField(null=True ,blank=True,)
    feccomp = models.DateField(null=True ,blank=True,)
    estcomp = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  #
    tipocomp = models.IntegerField(null=True ,blank=True,)
    abono = models.CharField(max_length=255, blank=True, null=True)
    uniqueid = models.CharField(max_length=20, blank=True, null=True)
    modo = models.CharField(max_length=255, blank=True, null=True)
    lista = models.CharField(max_length=255, blank=True, null=True)
    campain = models.CharField(max_length=255, blank=True, null=True)
    nopago = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Registro_Contacto'  # Especifica el nombre exacto de la tabla
        app_label = 'vnorte' 
        
class NewPhoneAvn(models.Model):
    lead_id = models.IntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  
    class Meta:
        managed = False 
        db_table = 'New_Phone'
        app_label = 'vnorte' 

class NewEmailAvn(models.Model):
    lead_id = models.IntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  

    class Meta:
        managed = False 
        db_table = 'New_Email'
        app_label = 'vnorte'


#global
class CarteraGlobal(models.Model):
    numerodocumento = models.CharField(max_length=10, null=True, blank=True)
    fecha_emi = models.DateField(null=True, blank=True)
    fecha_venc = models.DateField(null=True, blank=True)
    totalcomprobante = models.IntegerField(null=True, blank=True)
    numerocomprobante = models.IntegerField(null=True, blank=True)
    numerocomprobantefiscal = models.IntegerField(null=True, blank=True)
    tipocomprobantefiscal = models.CharField(max_length=2, null=True, blank=True)
    nombre = models.CharField(max_length=150, null=True, blank=True)
    morosidad = models.IntegerField(null=True, blank=True)
    calle = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    detalledomicilio = models.CharField(max_length=100, null=True, blank=True)
    comuna = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    id_documentos = models.CharField(max_length=20, null=True, blank=True)
    email = models.TextField(null=True, blank=True)  # Utilizar TextField para VARCHAR(MAX)
    fono = models.TextField(null=True, blank=True)  # Utilizar TextField para VARCHAR(MAX)
    tipo_envio = models.CharField(max_length=50, null=True, blank=True)
    tipo_cobranza = models.CharField(max_length=50, null=True, blank=True)
    emp_cobranza_id = models.IntegerField(null=True, blank=True)
    nom_emp_cobra = models.CharField(max_length=50, null=True, blank=True)
    refi = models.IntegerField(null=True, blank=True)
    pago0 = models.IntegerField(null=True, blank=True)
    dic20 = models.IntegerField(null=True, blank=True)
    dicom = models.IntegerField(null=True, blank=True)
    rutdv = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'Cartera'  # Asegúrate de que el nombre de la tabla coincida con la base de datos
        app_label = 'global'

class CarteraTotalesGlobal(models.Model):
    rut = models.CharField(max_length=10, null=True, blank=True)
    tipo_cobranza = models.CharField(max_length=50, null=True, blank=True)
    boletas = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    dias = models.IntegerField(null=True, blank=True)
    refi = models.IntegerField(null=True, blank=True)
    pago0 = models.IntegerField(null=True, blank=True)
    dic20 = models.IntegerField(null=True, blank=True)
    dicom = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Cartera_Totales'  # Especifica el nombre completo de la tabla
        app_label = 'global' 


class NewPhoneGlobal(models.Model):
    lead_id = models.IntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  
    class Meta:
        managed = False 
        db_table = 'New_Phone'
        app_label = 'global' 

class NewEmailGlobal(models.Model):
    lead_id = models.IntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  

    class Meta:
        managed = False 
        db_table = 'New_Email'
        app_label = 'global'

class RegistroContactoGlobal(models.Model):
    lead_id = models.IntegerField(null=True, blank=True)
    idrespuesta = models.IntegerField(null=True, blank=True)
    rut = models.CharField(max_length=11, null=True, blank=True)
    ruteje = models.CharField(max_length=12, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    glosa = models.CharField(max_length=255, null=True, blank=True)
    numdoc = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    feccomp = models.DateField(null=True, blank=True)
    estcomp = models.CharField(max_length=20, null=True, blank=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  
    tipocomp = models.IntegerField(null=True, blank=True)
    abono = models.CharField(max_length=255, null=True, blank=True)
    uniqueid = models.CharField(max_length=20, null=True, blank=True)
    modo = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Registro_Contacto'  # Asegúrate de que el nombre de la tabla coincida exactamente
        app_label = 'global'

#avo


class CarteraAVO(models.Model):
    idempresacobranza = models.IntegerField(null=True, blank=True)
    eceasignada = models.CharField(max_length=50, null=True, blank=True)
    mesasignacion = models.IntegerField(null=True, blank=True)
    campana = models.CharField(max_length=50, null=True, blank=True)
    idcampana = models.IntegerField(null=True, blank=True)
    descuento = models.TextField(null=True, blank=True)
    iddescuento = models.CharField(max_length=255, null=True, blank=True)
    segmento = models.CharField(max_length=50, null=True, blank=True)
    idsegmento = models.IntegerField(null=True, blank=True)
    grupocontrol = models.TextField(null=True, blank=True)
    idgrupocontrol = models.CharField(max_length=255, null=True, blank=True)
    judicial = models.TextField(null=True, blank=True)
    publicacion = models.TextField(null=True, blank=True)
    folio = models.IntegerField(null=True, blank=True)
    contrato = models.CharField(max_length=50, null=True, blank=True)
    rut = models.CharField(max_length=50, null=True, blank=True)
    rutsd = models.IntegerField(null=True, blank=True)
    representantelegal = models.TextField(null=True, blank=True)
    nombre = models.TextField(null=True, blank=True)
    grupofacturacion = models.TextField(null=True, blank=True)
    mediopago = models.CharField(max_length=50, null=True, blank=True)
    patentes = models.TextField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    consumomes = models.IntegerField(null=True, blank=True)
    cuotames = models.IntegerField(null=True, blank=True)
    estadorepactacion = models.CharField(max_length=100, null=True, blank=True)
    cuotasfuturas = models.CharField(max_length=100, null=True, blank=True)
    repactacion = models.CharField(max_length=100, null=True, blank=True)
    fechavencimiento = models.DateField(null=True, blank=True)
    fechafacturacion = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    complementodireccion = models.CharField(max_length=100, null=True, blank=True)
    comuna = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    telefono1 = models.CharField(max_length=50, null=True, blank=True)
    telefono2 = models.CharField(max_length=50, null=True, blank=True)
    mail = models.CharField(max_length=250, null=True, blank=True)
    tipodocumento = models.BinaryField(null=True, blank=True)
    mora = models.IntegerField(null=True, blank=True)
    tramomora = models.CharField(max_length=50, null=True, blank=True)
    tramomonto = models.CharField(max_length=50, null=True, blank=True)
    pago = models.CharField(max_length=1, null=True, blank=True),
    rutdv = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'Cartera'  # Asegúrate de que el nombre de la tabla coincida con la base de datos
        app_label = 'avo'
    
class CarteraTotalesAVO(models.Model):
    rut = models.CharField(max_length=10, null=True, blank=True)
    tipo_cobranza = models.CharField(max_length=50, null=True, blank=True)
    boletas = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    dias = models.IntegerField(null=True, blank=True)
    vence = models.DateField(null=True, blank=True)
    vence1 = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Cartera_Totales'  # Asegúrate de que el nombre de la tabla coincida con la base de datos
        app_label = 'avo'

class RegistroContactoAVO(models.Model):
    lead_id = models.IntegerField()
    idrespuesta = models.CharField(max_length=3, null=True, blank=True)
    rut = models.CharField(max_length=11, null=True, blank=True)
    ruteje = models.CharField(max_length=12, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    glosa = models.CharField(max_length=255, null=True, blank=True)
    numdoc = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    feccomp = models.DateField(null=True, blank=True)
    estcomp = models.CharField(max_length=20, null=True, blank=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  # Cambiado a CharField
    tipocomp = models.IntegerField(null=True, blank=True)
    abono = models.CharField(max_length=255, null=True, blank=True)
    uniqueid = models.CharField(max_length=20, null=True, blank=True)
    modo = models.CharField(max_length=255, null=True, blank=True)
    lista = models.CharField(max_length=255, null=True, blank=True)
    campain = models.CharField(max_length=255, null=True, blank=True)
    nopago = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Registro_Contacto'  # Asegúrate de que el nombre de la tabla coincida con la base de datos
        app_label = 'avo'

class NewPhoneAvo(models.Model):
    lead_id = models.IntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  
    class Meta:
        managed = False 
        db_table = 'New_Phone'
        app_label = 'avo' 

class NewEmailAvo(models.Model):
    lead_id = models.IntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  

    class Meta:
        managed = False 
        db_table = 'New_Email'
        app_label = 'avo'

#acsa
class CarteraACSA(models.Model):
    ic = models.IntegerField(null=True, blank=True)
    rut = models.CharField(max_length=10, null=True, blank=True)
    cod_cartera = models.CharField(max_length=34, null=True, blank=True)
    cc = models.CharField(max_length=12, null=True, blank=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    direccion_contractual = models.CharField(max_length=255, null=True, blank=True)
    comuna = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    direccion_facturacion = models.CharField(max_length=255, null=True, blank=True)
    comuna_f = models.CharField(max_length=255, null=True, blank=True)
    ciudad_f = models.CharField(max_length=255, null=True, blank=True)
    region_f = models.CharField(max_length=255, null=True, blank=True)
    fijo1 = models.CharField(max_length=255, null=True, blank=True)
    fijo2 = models.CharField(max_length=255, null=True, blank=True)
    fijo3 = models.CharField(max_length=255, null=True, blank=True)
    movil1 = models.CharField(max_length=255, null=True, blank=True)
    movil2 = models.CharField(max_length=255, null=True, blank=True)
    movil3 = models.CharField(max_length=255, null=True, blank=True)
    email1 = models.CharField(max_length=255, null=True, blank=True)
    email2 = models.CharField(max_length=255, null=True, blank=True)
    email3 = models.CharField(max_length=255, null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    contador = models.IntegerField(null=True, blank=True)
    tipo_cobranza = models.CharField(max_length=10, null=True, blank=True)
    dias = models.IntegerField(null=True, blank=True)
    cesion = models.IntegerField(null=True, blank=True)
    honorario = models.IntegerField(null=True, blank=True)
    vigente = models.CharField(max_length=5, null=True, blank=True)
    ptt = models.BooleanField(null=True, blank=True)  # TINYINT suele usarse para booleanos en otros sistemas
    ruta = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Cartera'  # Asegúrate de que el nombre de la tabla coincida con la base de datos
        app_label = 'acsa'

class PagosAcsa(models.Model):
    rut = models.CharField(max_length=10, null=True, blank=True)
    ic = models.IntegerField(null=True, blank=True)
    pago = models.IntegerField(null=True, blank=True)
    fecha_informe = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Pagos'  # Nombre exacto de la tabla en la base de datos
        app_label = 'acsa' 

class RegistroContactoAcsa(models.Model):
    lead_id = models.IntegerField(null=True)
    idrespuesta = models.CharField(max_length=3, blank=True, null=True)
    rut = models.CharField(max_length=11, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    glosa = models.CharField(max_length=255, blank=True, null=True)
    numdoc = models.IntegerField(blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    feccomp = models.DateField(blank=True, null=True)
    estcomp = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  #
    tipocomp = models.IntegerField(blank=True, null=True)
    abono = models.CharField(max_length=255, blank=True, null=True)
    uniqueid = models.CharField(max_length=20, blank=True, null=True)
    modo = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'Registro_Contacto'  # Asegura que Django utilice el nombre correcto de la tabla
        managed = False 
        app_label = 'acsa'


class Descuento(models.Model):
    origen = models.CharField(max_length=10, null=True)
    rut = models.CharField(max_length=50, null=True)
    ic = models.IntegerField(null=True)
    cc = models.IntegerField(null=True)
    deuda_total = models.CharField(max_length=20, null=True)
    descuento_total = models.CharField(max_length=20, null=True)
    tipo_descuento = models.CharField(max_length=20, null=True)
    Tp_Dcto = models.CharField(max_length=20, null=True)
    Nombre_Camp = models.CharField(max_length=50, null=True)
    Dcto_Extraordinario = models.CharField(max_length=20, null=True)
    class Meta:
        db_table = 'Descuento'
        managed = False
        app_label = 'acsa'


class BoletaAcsa(models.Model):
    mandante = models.CharField(max_length=3, null=True, blank=True)
    nsap = models.CharField(max_length=12, null=True, blank=True)
    posicion_cobro = models.CharField(max_length=3, null=True, blank=True)
    ic = models.IntegerField(null=True, blank=True)
    cc = models.CharField(max_length=12, null=True, blank=True)
    moneda = models.CharField(max_length=5, null=True, blank=True)
    monto = models.CharField(max_length=16, null=True, blank=True)
    n_doc_pago = models.CharField(max_length=12, null=True, blank=True)
    cod_tipo_car = models.CharField(max_length=10, null=True, blank=True)
    cod_vinculo = models.CharField(max_length=24, null=True, blank=True)
    cod_cartera = models.CharField(max_length=34, null=True, blank=True)
    cartera_especial = models.CharField(max_length=1, null=True, blank=True)
    tramo_mora = models.CharField(max_length=13, null=True, blank=True)
    folio = models.CharField(max_length=16, null=True, blank=True)
    clase_doc = models.CharField(max_length=2, null=True, blank=True)
    fecha_doc = models.CharField(max_length=8, null=True, blank=True)
    fecha_venc = models.CharField(max_length=8, null=True, blank=True)
    sector_deuda = models.CharField(max_length=2, null=True, blank=True)
    castigo = models.CharField(max_length=1, null=True, blank=True)
    ppu = models.CharField(max_length=25, null=True, blank=True)
    cta_mayor = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'Boleta'
        managed = False
        app_label = 'acsa'
        

class NewPhoneAcsa(models.Model):
    lead_id = models.IntegerField()
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  
    class Meta:
        managed = False 
        db_table = 'New_Phone'
        app_label = 'acsa' 

class NewEmailAcsa(models.Model):
    lead_id = models.IntegerField()
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  

    class Meta:
        managed = False 
        db_table = 'New_Email'
        app_label = 'acsa'

#cnorte
class CarteraCnorte(models.Model):
    tipo_cobranza = models.CharField(max_length=2, null=True, blank=True)
    num_doc = models.BigIntegerField(null=True, blank=True)
    tipo_doc = models.CharField(max_length=2, null=True, blank=True)
    monto_doc = models.BigIntegerField(null=True, blank=True)
    tipo_deudor = models.CharField(max_length=1, null=True, blank=True)
    rut = models.CharField(max_length=10, null=True, blank=True)
    cod_cliente = models.CharField(max_length=17, null=True, blank=True)
    nombres = models.CharField(max_length=30, null=True, blank=True)
    apellido_pat = models.CharField(max_length=20, null=True, blank=True)
    apellido_mat = models.CharField(max_length=20, null=True, blank=True)
    direc_calle = models.CharField(max_length=50, null=True, blank=True)
    direc_puerta = models.CharField(max_length=10, null=True, blank=True)
    direc_detalle = models.CharField(max_length=30, null=True, blank=True)
    cod_postal = models.CharField(max_length=7, null=True, blank=True)
    comuna = models.CharField(max_length=20, null=True, blank=True)
    region = models.CharField(max_length=3, null=True, blank=True)
    ciudad = models.CharField(max_length=20, null=True, blank=True)
    fono1 = models.CharField(max_length=15, null=True, blank=True)
    fono2 = models.CharField(max_length=15, null=True, blank=True)
    movil = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    fec_facturacion = models.CharField(max_length=8, null=True, blank=True)
    fec_vence = models.CharField(max_length=8, null=True, blank=True)
    ajuste_anterior = models.BigIntegerField(null=True, blank=True)
    ajuste_actual = models.BigIntegerField(null=True, blank=True)
    total_a_pagar = models.BigIntegerField(null=True, blank=True)
    rutdv = models.CharField(max_length=11, null=True, blank=True)
    fec_fac1 = models.DateTimeField(null=True, blank=True)
    fec_vence1 = models.DateTimeField(null=True, blank=True)
    cod = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'cartera'  # Asegúrate de que el nombre de la tabla coincida con la base de datos
        app_label = 'cnorte'


class CarteraTotalesCnorte(models.Model):
    rut = models.CharField(max_length=11, null=True, blank=True)
    tipo_cobranza = models.CharField(max_length=50, null=True, blank=True)
    boletas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vence = models.DateField(null=True, blank=True)
    vence1 = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Cartera_Totales'  # Asegúrate de que el nombre de la tabla coincida con la base de datos
        app_label = 'cnorte'

class RegistroContactoCnorte(models.Model):
    lead_id = models.IntegerField()
    idrespuesta = models.CharField(max_length=3, null=True, blank=True)
    rut = models.CharField(max_length=11, null=True, blank=True)
    ruteje = models.CharField(max_length=12, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    glosa = models.CharField(max_length=255, null=True, blank=True)
    numdoc = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    feccomp = models.DateField(null=True, blank=True)
    estcomp = models.CharField(max_length=20, null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)
    tipocomp = models.IntegerField(null=True, blank=True)
    abono = models.CharField(max_length=255, null=True, blank=True)
    uniqueid = models.CharField(max_length=20, null=True, blank=True)
    modo = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Registro_Contacto'  # Asegúrate de que el nombre de la tabla coincida exactamente
        app_label = 'cnorte'

#vsur
class CarteraVsur(models.Model):
    tipo_cobranza = models.CharField(max_length=2, null=True, blank=True)
    num_doc = models.BigIntegerField(null=True, blank=True)
    tipo_doc = models.CharField(max_length=2, null=True, blank=True)
    monto_doc = models.BigIntegerField(null=True, blank=True)
    tipo_deudor = models.CharField(max_length=1, null=True, blank=True)
    rut = models.CharField(max_length=10, null=True, blank=True)
    cod_cliente = models.CharField(max_length=17, null=True, blank=True)
    nombres = models.CharField(max_length=30, null=True, blank=True)
    apellido_pat = models.CharField(max_length=20, null=True, blank=True)
    apellido_mat = models.CharField(max_length=20, null=True, blank=True)
    direc_calle = models.CharField(max_length=50, null=True, blank=True)
    direc_puerta = models.CharField(max_length=10, null=True, blank=True)
    direc_detalle = models.CharField(max_length=30, null=True, blank=True)
    cod_postal = models.CharField(max_length=7, null=True, blank=True)
    comuna = models.CharField(max_length=20, null=True, blank=True)
    region = models.CharField(max_length=3, null=True, blank=True)
    ciudad = models.CharField(max_length=20, null=True, blank=True)
    fono1 = models.CharField(max_length=15, null=True, blank=True)
    fono2 = models.CharField(max_length=15, null=True, blank=True)
    movil = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    fec_facturacion = models.CharField(max_length=8, null=True, blank=True)
    fec_vence = models.CharField(max_length=8, null=True, blank=True)
    ajuste_anterior = models.BigIntegerField(null=True, blank=True)
    ajuste_actual = models.BigIntegerField(null=True, blank=True)
    total_a_pagar = models.BigIntegerField(null=True, blank=True)
    rutdv = models.CharField(max_length=11, null=True, blank=True)
    fec_fac1 = models.DateTimeField(null=True, blank=True)
    fec_vence1 = models.DateTimeField(null=True, blank=True)
    cod = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'cartera'  # Asegúrate de que el nombre de la tabla coincida exactamente
        app_label = 'vsur'

class CarteraTotalesVsur(models.Model):
    rut = models.CharField(max_length=11, null=True, blank=True)
    tipo_cobranza = models.CharField(max_length=50, null=True, blank=True)
    boletas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vence = models.DateField(null=True, blank=True)
    vence1 = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Cartera_Totales'  # Asegúrate de que el nombre de la tabla coincida exactamente
        app_label = 'vsur'

class RegistroContactoVsur(models.Model):
    lead_id = models.IntegerField()
    idrespuesta = models.CharField(max_length=3, null=True, blank=True)
    rut = models.CharField(max_length=11, null=True, blank=True)
    ruteje = models.CharField(max_length=12, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    glosa = models.CharField(max_length=255, null=True, blank=True)
    numdoc = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    feccomp = models.DateField(null=True, blank=True)
    estcomp = models.CharField(max_length=20, null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)
    tipocomp = models.IntegerField(null=True, blank=True)
    abono = models.CharField(max_length=255, null=True, blank=True)
    uniqueid = models.CharField(max_length=20, null=True, blank=True)
    modo = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Registro_Contacto'  
        app_label = 'vsur'  

#report
class TipificacionesReport(models.Model):
    glosa_gestion = models.CharField(max_length=100, blank=True, null=True)
    glosa_estado = models.CharField(max_length=100, blank=True, null=True)
    idrespuesta = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False  # Django no manejará la creación de la tabla
        db_table = 'Tipificaciones'
        app_label = 'report'

class TipificacionesApi(models.Model):
    glosa_gestion = models.CharField(max_length=100, blank=True, null=True)
    glosa_estado = models.CharField(max_length=100, blank=True, null=True)
    idrespuesta = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False  # Django no manejará la creación de la tabla
        db_table = 'Tipificaciones'
        app_label = 'pass'
        
        
class User(models.Model):
    idempresa = models.IntegerField(null=True, blank=True, default=None)
    name = models.CharField(max_length=100, null=True, blank=True, default=None)
    campaign_id = models.CharField(max_length=20, null=True, blank=True, default=None)
    list_id = models.IntegerField(null=True, blank=True, default=None)
    password = models.CharField(max_length=50, null=True, blank=True, default=None)
    level = models.IntegerField(null=True, blank=True, default=None)
    active = models.SmallIntegerField(null=True, blank=True, default=None)
    user_konecsys = models.CharField(max_length=255, null=True, blank=True, default=None)
    menu_konecsys = models.TextField(null=True, blank=True)
    fecha_ing = models.CharField(max_length=255, null=True, blank=True, default=None)
    sesion = models.CharField(max_length=255, null=True, blank=True, default=None)
    monitor = models.CharField(max_length=255, null=True, blank=True, default=None)

    class Meta:
        db_table = 'users'
        managed = False
        app_label = 'report'

# audios 




class RegistroContactoCondeza(models.Model):
    lead_id = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    idrespuesta = models.CharField(max_length=3, null=True, blank=True)
    rut = models.CharField(max_length=11, null=True, blank=True)
    ruteje = models.CharField(max_length=12, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    glosa = models.CharField(max_length=255, null=True, blank=True)
    numdoc = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    feccomp = models.DateField(null=True, blank=True)
    estcomp = models.CharField(max_length=20, null=True, blank=True)
    fecha = models.CharField(max_length=25, null=True, blank=True) 
    tipocomp = models.IntegerField(null=True, blank=True)
    abono = models.CharField(max_length=255, null=True, blank=True)
    uniqueid = models.CharField(max_length=20, null=True, blank=True)
    modo = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Registro_Contacto'
        app_label = 'condeza'

class NewPhoneCondeza(models.Model):
    lead_id = models.IntegerField()
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  
    class Meta:
        managed = False 
        db_table = 'New_Phone'
        app_label = 'condeza' 

class NewEmailCondeza(models.Model):
    lead_id = models.IntegerField()
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  

    class Meta:
        managed = False 
        db_table = 'New_Email'
        app_label = 'condeza'

class CodigoRespuesta(models.Model):
    id = models.CharField(max_length=3,null=True)
    respuesta = models.CharField(max_length=255)
    tipo = models.CharField(max_length=2)
    pond = models.IntegerField()
    is_visible_crm = models.IntegerField()
    active = models.IntegerField()
    class Meta:
        managed = False 
        db_table = 'Codigo_Respuesta'
        app_label = 'condeza'


class Logs(models.Model):
    uniqueid = models.CharField(max_length=50, null=True, blank=True)
    lead_id = models.IntegerField(null=True, blank=True)
    list_id = models.IntegerField(null=True, blank=True)
    campaign_id = models.CharField(max_length=50, null=True, blank=True)
    call_date = models.DateTimeField(null=True, blank=True)
    length_in_sec = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    phone_code = models.IntegerField(null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    user = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    processed = models.CharField(max_length=1, null=True, blank=True)
    user_group = models.CharField(max_length=50, null=True, blank=True)
    term_reason = models.CharField(max_length=50, null=True, blank=True)
    called_count = models.IntegerField(null=True, blank=True)
    entry_date = models.DateTimeField(null=True, blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    vendor_lead_code = models.CharField(max_length=50, null=True, blank=True)
    source_id = models.CharField(max_length=50, null=True, blank=True)
    gmt_offset_now = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    called_since_last_reset = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_initial = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    address3 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    alt_phone = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    security_phrase = models.CharField(max_length=255, null=True, blank=True)
    last_local_call_time = models.DateTimeField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    owner = models.CharField(max_length=50, null=True, blank=True)
    entry_list_id = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Logs'
        managed = False  # Si la tabla ya existe en la base de datos y no debe ser gestionada por Django
        app_label = 'vici'

class Bliblioteca(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)
    active = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Bliblioteca'
        managed = False

class VolverLlamar(models.Model):
    Rut = models.CharField(max_length=50, null=True)
    Ruteje = models.CharField(max_length=50, null=True)
    Fecha_Gestion = models.CharField(max_length=25, null=True, blank=True)
    Fecha_Agenda = models.CharField(max_length=25, null=True, blank=True)
    Prefix = models.CharField(max_length=50, null=True)
    monto = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    glosa = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'Volver_Llamar'
        app_label = 'storage'
        managed = False
        
class UserLogin(models.Model):
    idUser = models.AutoField(primary_key=True, db_column='idUser')
    NameUser = models.CharField(max_length=50, null=True, db_column='NameUser')
    Correo = models.CharField(max_length=50, null=True, db_column='Correo')
    Password = models.CharField(max_length=50, null=True, db_column='Password')  # Considera almacenar contraseñas encriptadas
    idArea = models.IntegerField(null=True, db_column='idArea')
    idRol = models.IntegerField(null=True, db_column='idRol')
    Rut = models.CharField(max_length=50, null=True, db_column='Rut')
    token = models.TextField(null=True, db_column='token')
    dateCreation = models.DateField(null=True, db_column='dateCreation')

    class Meta:
        db_table = 'Users'
        managed = False  # Si la tabla ya existe en la base de datos y no debe ser
        app_label = 'api'

class RegistroContactoPass(models.Model):
    lead_id = models.IntegerField(null=True)
    idrespuesta = models.CharField(max_length=3, blank=True, null=True)
    rut = models.CharField(max_length=11, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    glosa = models.CharField(max_length=255, blank=True, null=True)
    numdoc = models.IntegerField(blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    feccomp = models.DateField(blank=True, null=True)
    estcomp = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  #
    tipocomp = models.IntegerField(blank=True, null=True)
    abono = models.CharField(max_length=255, blank=True, null=True)
    uniqueid = models.CharField(max_length=20, blank=True, null=True)
    modo = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'Registro_Contacto'  # Asegura que Django utilice el nombre correcto de la tabla
        managed = False 
        app_label = 'pass'

class CarteraPass(models.Model):
    document_invoicing_type_id = models.IntegerField(null=True, blank=True)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    customer_nid = models.CharField(max_length=200, null=True, blank=True)
    contract_concession_id = models.IntegerField(null=True, blank=True)
    contract_concession_rnut_code = models.CharField(max_length=100, null=True, blank=True)
    document_type = models.CharField(max_length=200, null=True, blank=True)
    document_legal_number = models.BigIntegerField(null=True, blank=True)
    document_issue_date = models.DateField(null=True, blank=True)
    document_expiration_date = models.DateField(null=True, blank=True)
    tolling_amount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    interests_exempt_amount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    interests_affect_amount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    collection_expenses_amount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    adjusts_amount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    refinancing_interests_amount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    refinancing_pastdue_interests_amount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    obu_quotas_amount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    obu_quotas_compensations_amount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    document_total = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    document_total_tax = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    document_grand_total = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    saldo = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    personeria = models.CharField(max_length=100, null=True, blank=True)
    fono1_nativo = models.CharField(max_length=50, null=True, blank=True)
    fono2_nativo = models.CharField(max_length=50, null=True, blank=True)
    fono3_nativo = models.CharField(max_length=50, null=True, blank=True)
    fono1_rnut = models.CharField(max_length=50, null=True, blank=True)
    fono2_rnut = models.CharField(max_length=50, null=True, blank=True)
    fono3_rnut = models.CharField(max_length=50, null=True, blank=True)
    mail1_nativo = models.CharField(max_length=150, null=True, blank=True)
    mail2_nativo = models.CharField(max_length=150, null=True, blank=True)
    mail3_nativo = models.CharField(max_length=150, null=True, blank=True)
    mail1_rnut = models.CharField(max_length=150, null=True, blank=True)
    mail2_rnut = models.CharField(max_length=150, null=True, blank=True)
    mail3_rnut = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    complemento = models.IntegerField(null=True, blank=True)
    comuna = models.CharField(max_length=150, null=True, blank=True)
    Región = models.CharField(max_length=150, null=True, blank=True)
    mora = models.IntegerField(null=True, blank=True)
    monto_rut = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    mora_rut = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    RutSDV = models.IntegerField(null=True, blank=True)
    cobranza = models.CharField(max_length=50, null=True, blank=True)
    tramo_mora = models.CharField(max_length=150, null=True, blank=True)
    tramo_monto = models.CharField(max_length=150, null=True, blank=True)
    ece = models.CharField(max_length=150, null=True, blank=True)
    marca = models.CharField(max_length=150, null=True, blank=True)
    cesion = models.CharField(max_length=150, null=True, blank=True)
    cluster = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    refinanciacion = models.CharField(max_length=50, null=True, blank=True)
    inhabilitacion = models.CharField(max_length=50, null=True, blank=True)
    castigo = models.CharField(max_length=150, null=True, blank=True)
    demanda = models.CharField(max_length=50, null=True, blank=True)
    publicacion_financiera = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'Cartera'
        managed = False 
        app_label = 'pass'

class NewPhonePass(models.Model):
    lead_id = models.IntegerField()
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  
    class Meta:
        managed = False 
        db_table = 'New_Phone'
        app_label = 'pass' 

class NewEmailPass(models.Model):
    lead_id = models.IntegerField()
    rut = models.CharField(max_length=12, blank=True, null=True)
    ruteje = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.CharField(max_length=25, null=True, blank=True)  

    class Meta:
        managed = False 
        db_table = 'New_Email'
        app_label = 'pass'
        
class RegistroContactoAutoriza(models.Model):
    lead_id = models.IntegerField()
    idrespuesta = models.CharField(max_length=3, null=True, blank=True)
    rut = models.CharField(max_length=11, null=True, blank=True)
    ruteje = models.CharField(max_length=12, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    glosa = models.CharField(max_length=255, null=True, blank=True)
    numdoc = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    feccomp = models.DateField(null=True, blank=True)
    estcomp = models.CharField(max_length=20, null=True, blank=True)
    fecha = models.CharField(null=True, blank=True)
    tipocomp = models.IntegerField(null=True, blank=True)
    abono = models.CharField(max_length=255, null=True, blank=True)
    uniqueid = models.CharField(max_length=20, null=True, blank=True)
    modo = models.CharField(max_length=255, null=True, blank=True)
    prefix = models.CharField(max_length=255, null=True, blank=True)
    autorizo = models.CharField(max_length=255, null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    autorizaDate = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        db_table = 'AutorizaLLamado'  
        app_label = 'storage'