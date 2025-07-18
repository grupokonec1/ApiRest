from django.shortcuts import render
from django.db import connections,DatabaseError
import requests
from django.conf import settings
from io import BytesIO
# Create your views here.
# Api/views.py
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import VolverLlamar,TipificacionesApi,RegistroContactoAutoriza,NewEmailPass,NewPhonePass,RegistroContactoPass,CarteraPass,CarteraGlobal,CodigoRespuesta,NewPhoneCondeza,NewEmailCondeza,RegistroContactoCondeza,NewEmailSvia,NewPhoneSvia,NewEmailAvo,NewEmailAvn,NewPhoneAvn,NewPhoneAvo,NewPhoneAcsa,NewEmailAcsa,NewPhoneGlobal,BoletaAcsa,NewEmailGlobal,RegistroContactoAcsa,TipificacionesReport,CarteraAVO,RegistroContactoVnort, RegistroContacto,Cartera,CarteraTotales, CarteraVnort,PagosAcsa,RegistroContactoAVO
from .serializers import TipificacionSerializerApi,RegistroContactoAutorizaLLamadoSerializer,CarteraPassSerializer,NewEmailPassSerializer,NewPhonoPassSerializer,InsertaCallAgain,RegistroContactoPassSerializer,TipificacionCondezaSerializerReport,NewPhonoGlobalSerializer,NewEmailCondezaSerializer,NewPhonoCondezaSerializer,RegistroContactoCondezaSerializer,NewEmailSviaSerializer,NewPhonoSviaSerializer,NewEmailAvnSerializer,NewPhonoAvnSerializer,NewPhonoAvoSerializer,NewEmailAvoSerializer,NewEmailAcsaSerializer,NewPhonoAcsaSerializer,BoletaAcsaSerializer,NewEmailGlobalSerializer,RegistroContactoGlobal,CarteraGlobalSerializer,CarteraAcsaSerializer,CarteraGlobal,RegistroContactoAcsaSerializer,TipificacionSerializerReport,CarteraAvoSerializer,RegistroContactoAvoSerializer,RegistroContactoGlobalSerializer,RegistroContactoVnortSerializer,RegistroContactoSerializer,PagosAcsaSerializer,CarteraSerializer,CarteraTotalesSerializer, CarteraVnortSerializer
from datetime import datetime
from collections import defaultdict
from rest_framework.decorators import api_view
from smb.SMBConnection import SMBConnection
from django.http import HttpResponse, Http404, JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.html import strip_tags

class ListarTipificacionesRepoort(generics.ListAPIView):
    queryset = TipificacionesReport.objects.all()
    serializer_class = TipificacionSerializerReport

class ListarTipificacionesApi(generics.ListAPIView):
    queryset = TipificacionesApi.objects.all()
    serializer_class = TipificacionSerializerApi

class ContactByRUT(APIView):
    def get(self, request, rutdv):
        
        contacts = Cartera.objects.filter(rutdv=rutdv)  
        serializer = CarteraSerializer(contacts, many=True)
        return Response(serializer.data)
        
class InsertarRegistroContacto(generics.CreateAPIView):
    queryset = RegistroContacto.objects.all()
    serializer_class = RegistroContactoSerializer


class ConsultaRutView(APIView):
    def get(self, request, rutdv):
        with connections['svia'].cursor() as cursor:
            cursor.execute("""          
                SELECT
                    ct.RutDV AS RUT,
                    MAX(ct.boletas) AS BOLETAS,
                    MAX(ct.monto) AS MONTO,
                    MAX(c.Nombre) AS NOMBRE,
                    MAX(c.Email) AS EMAIL,
                    MAX(c.comuna) AS COMUNA,
                    MAX(c.Direccion) AS direccion,
                    MAX(c.Region) AS region,
                    max(c.Fono_2) AS fono1,
                    max(c.Fono_3) AS fono2,
                    max(c.Fono_4) AS fono3,
                    max(c.Celular)AS Celular,
                    max(c.Tramo_Mora) AS tramo
                FROM 
                    cartera_totales ct WITH (NOLOCK)
                JOIN 
                    cartera c  WITH (NOLOCK) ON ct.RutDV = c.RutDV
                WHERE 
                    c.RutDV = %s
                GROUP BY 
                    ct.RutDV
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    

class CarterTotalesByRUT(APIView):
    def get(self, request, rutdv):
        contacts = CarteraTotales.objects.filter(rutdv=rutdv)  
        serializer = CarteraTotalesSerializer(contacts, many=True)
        return Response(serializer.data)
    
class InsertarNewPhonoSvia(generics.CreateAPIView):
    queryset = NewPhoneSvia.objects.all()
    serializer_class = NewPhonoSviaSerializer

class InsertarNewEmailSvia(generics.CreateAPIView):
    queryset = NewEmailSvia.objects.all()
    serializer_class = NewEmailSviaSerializer
    


#api

#avn no se esta utilizando

class ConsultaRutViewVnorte(APIView):
    def get(self, request, rutdv):
        cursor = connections['vnorte'].cursor()
        try:
            cursor.execute("""
                SELECT
                    ct.rut AS RUT,
                    MAX(ct.boletas) AS BOLETAS,
                    MAX(ct.monto) AS MONTO,
                    MAX(c.Razon_Social) AS NOMBRE,
                    MAX(c.Email) AS EMAIL,
                    MAX(c.comuna) AS COMUNA,
                    MAX(c.Region) AS DETALLE_DOMICILIO,
                    MAX(c.Fono_1) AS fono1,
                    MAX(c.Fono_2) AS fono2
                FROM
                    cartera_totales ct
                JOIN 
                    cartera c ON ct.rut = c.rut
                WHERE 
                    c.rut = %s
                GROUP BY 
                    ct.rut
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)

class ContactByRUTvnort(APIView):
    def get(self, request, rut):  
        contacts = CarteraVnort.objects.filter(rut=rut)  
        serializer = CarteraVnortSerializer(contacts, many=True)
        return Response(serializer.data)
    
            
class InsertarRegistroContactoVnort(generics.CreateAPIView):
    queryset = RegistroContactoVnort.objects.all()
    serializer_class = RegistroContactoVnortSerializer

    
class InsertarNewPhonoAvn(generics.CreateAPIView):
    queryset = NewPhoneAvn.objects.all()
    serializer_class = NewPhonoAvnSerializer

class InsertarNewEmailAvn(generics.CreateAPIView):
    queryset = NewEmailAvn.objects.all()
    serializer_class = NewEmailAvnSerializer

#--------

# avo
class InsertarRegistroContactoAvo(generics.CreateAPIView):
    queryset = RegistroContactoAVO.objects.all()
    serializer_class = RegistroContactoAvoSerializer

class ConsultaRutViewAvo(APIView):
    def get(self, request, rutdv):
        cursor = connections['avo'].cursor()
        try:
            cursor.execute("""
                SELECT
        ct.rutDV AS RUT,
         
                    MAX(ct.boletas) AS BOLETAS,
                    MAX(ct.monto) AS MONTO,
                    MAX(c.Nombre) AS NOMBRE,
                    MAX(c.Mail) AS EMAIL,
                    MAX(c.comuna) AS COMUNA,
                    MAX(c.Repactacion) AS Repactacion,
                    MAX(c.Region) AS Region,
                    MAX(c.ComplementoDireccion) AS direccion,
                    max(c.Telefono1) AS fono1,
                    max(c.Telefono2) AS fono2,
                    max(c.Publicacion) AS dicom
                FROM 
                    cartera_totales ct WITH (NOLOCK)
                JOIN 
                    cartera c WITH (NOLOCK) ON ct.rutDV = c.RutDV
                WHERE 
                    c.RutDV = %s
                GROUP BY 
                    ct.rutDV
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    
class ContactByRUTAvo(APIView):
    def get(self, request, rutdv):
        contacts =CarteraAVO.objects.filter(rutdv=rutdv)  
        serializer = CarteraAvoSerializer(contacts, many=True)
        return Response(serializer.data)

class InsertarNewPhonoAvo(generics.CreateAPIView):
    queryset = NewPhoneAvo.objects.all()
    serializer_class = NewPhonoAvoSerializer

class InsertarNewEmailAvo(generics.CreateAPIView):
    queryset = NewEmailAvo.objects.all()
    serializer_class = NewEmailAvoSerializer

#falta
class ConsultaViewPatenteAvo(APIView):
    def get(self, request, rutdv):
        cursor = connections['avo'].cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT CAST(Patentes AS VARCHAR(MAX)) AS Patentes 
                FROM AVO.dbo.Cartera WITH (NOLOCK) WHERE RutDV = %s;
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)

class getDescuentoAvo(APIView):
    def get(self, request, rutdv):
        cursor = connections['avo'].cursor()
        try:
            cursor.execute("""
                SELECT SUM(Monto) AS MontoReal, SUM(Descuento)as descuento, SUM(MontoaPagar) AS allPaid FROM AVO.dbo.Descuento WITH (NOLOCK) WHERE RutDV= %s
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)
    

#acsa
class InsertarRegistroContactoAcsa(generics.CreateAPIView):
    queryset = RegistroContactoAcsa.objects.all()
    serializer_class = RegistroContactoAcsaSerializer

class GetGrupoFacturacionAcsa(APIView): 
    def get(self, request, ic):
        cursor = connections['acsa'].cursor()
        try:
            cursor.execute("""
                SELECT cc,Grupo,Fecha_Facturacion,Fecha_Vencimiento FROM vw_grupo_facturacion where ic = %s
            """, [ic])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)
    
class getChequesAcsa(APIView): 
    def get(self, request, rut):
        cursor = connections['acsa'].cursor()
        try:
            cursor.execute("""
                SELECT N_cheque, Fecha_ven_cheque, Importe_pago FROM ACSA.dbo.Cheque where Rut_Cli = %s
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)


class ConsultaRutViewAcsa(APIView):
    def get(self, request, rutdv):
        cursor = connections['acsa'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM ACSA.dbo.Cartera WITH (NOLOCK) WHERE rutdv = %s
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)
    
    

    

    
class ListarPagosAcsa(generics.ListAPIView):
    queryset = PagosAcsa.objects.all()
    serializer_class = PagosAcsaSerializer


class InsertarNewPhonoAcsa(generics.CreateAPIView):
    queryset = NewPhoneAcsa.objects.all()
    serializer_class = NewPhonoAcsaSerializer

class InsertarNewEmailAcsa(generics.CreateAPIView):
    queryset = NewEmailAcsa.objects.all()
    serializer_class = NewEmailAcsaSerializer

class ListarBotetaAcsa(APIView):
    def get(self, request, rutdv):
        cursor = connections['acsa'].cursor()
        try:
            cursor.execute("""
                SELECT  b.monto,b.ppu,b.sector_deuda,b.fecha_doc,b.fecha_venc,b.folio,b.cc
 FROM boleta b  WITH (NOLOCK)
 INNER JOIN
 cartera c WITH (NOLOCK) ON b.ic = c.ic WHERE c.rut = %s
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)

class ListarDescuentoAcsa(APIView):
    def get(self, request, rutdv):
        cursor = connections['acsa'].cursor()
        try:
            cursor.execute("""
                SELECT descuento_total FROM  vw_descuento_new WITH (NOLOCK) WHERE rut = %s
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    
class PagoAutomaticoAcsa(APIView):
    def get(self, request, ic):
        cursor = connections['acsa'].cursor()
        try:
            cursor.execute("""
                select ic from [pago_automatico] where ic = %s
            """, [ic])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)


class ConveniosAcsa(APIView):
    def get(self, request, rut):
        cursor = connections['acsa'].cursor()
        try:
            cursor.execute("""
                select Saldo_Impago,Valor_Cuota,Cuotas_restantes from Convenios where  Rut = %s
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    
class InhabilitadosAcsa(APIView):
    def get(self, request, ic):
        cursor = connections['acsa'].cursor()
        try:
            cursor.execute("""
                select Fecha_Desconect from Cliente_Inhablita where Socio_comercial = %s
            """, [ic])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    

class ListarPpuAcsa(APIView):
    def get(self, request, rutdv):
        cursor = connections['acsa'].cursor()
        try:
            cursor.execute("""
                SELECT 
  p.cod_cartera,
  p.ic,
  p.cc,
  p.PPU
FROM ACSA.dbo.PPU p WITH (NOLOCK) 
INNER JOIN Cartera c WITH (NOLOCK) ON p.ic= c.ic WHERE c.rut = %s
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    

#global

class ConsultaRutViewGlobal(APIView):
    def get(self, request, rutdv):
        cursor = connections['global'].cursor()
        try:
            cursor.execute("""
                SELECT
        ct.rutDV AS RUT,
         
                    MAX(ct.boletas) AS BOLETAS,
                    MAX(ct.monto) AS MONTO,
                    MAX(c.Nombre) AS NOMBRE,
                    MAX(c.Email) AS EMAIL,
                    MAX(c.comuna) AS COMUNA,
                    MAX(c.Region) AS Region,
                    max(c.Calle) AS direccion,
                    max(c.Fono) AS Fono,
                    max(c.tipo_cobranza) AS tramo
                FROM 
                    cartera_totales ct WITH (NOLOCK) 
                JOIN 
                    cartera c WITH (NOLOCK) ON ct.rutDV = c.RutDV
                WHERE
                    c.RutDV = %s
                GROUP BY 
                    ct.rutDV
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    

class ContactByRUTGlobal(APIView):
    def get(self, request, rutdv):
        contacts =CarteraGlobal.objects.filter(rutdv=rutdv)  
        serializer = CarteraGlobalSerializer(contacts, many=True)
        return Response(serializer.data)
    

class InsertarRegistroContactoGlobal(generics.CreateAPIView):
    queryset = RegistroContactoGlobal.objects.all()
    serializer_class = RegistroContactoGlobalSerializer


class InsertarNewPhonoGlobal(generics.CreateAPIView):
    queryset = NewPhoneGlobal.objects.all()
    serializer_class = NewPhonoGlobalSerializer

class InsertarNewEmailGlobal(generics.CreateAPIView):
    queryset = NewEmailGlobal.objects.all()
    serializer_class = NewEmailGlobalSerializer

    
class ConsultaRutUserView(APIView):
    def get(self, request, rutdv):
        cursor = connections['report'].cursor()
        try:
            cursor.execute("""
                SELECT u.rut, u.nombre, u.idroles FROM report00.dbo.new_usuers u WHERE u.rut = %s
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)



class ConsultaRutViewCondeza(APIView):
    def get(self, request, rutdv):
        cursor = connections['condeza'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM Cartera WITH (NOLOCK) WHERE RUTDV = %s
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    

class InsertarRegistroContactoCondeza(generics.CreateAPIView):
    queryset = RegistroContactoCondeza.objects.all()
    serializer_class = RegistroContactoCondezaSerializer
    

class ListarGestionesCondeza(APIView):
    def get(self, request, rutdv):
        cursor = connections['condeza'].cursor()
        try:
            cursor.execute("""
                SELECT top 15 
rc.fecha,
crc.tipo,
crc.respuesta,
rc.feccomp,
rc.ruteje,
rc.glosa
FROM Registro_Contacto rc WITH (NOLOCK)
INNER JOIN codigo_respuesta_condeza crc WITH (NOLOCK)
on rc.idrespuesta = crc.id WHERE rc.rut = %s
ORDER BY rc.fecha DESC
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

        # Formatear las fechas
        result_list = []
        for row in data:
            row_dict = dict(zip(columns, row))
            for key in ['fecha', 'feccomp']:
                if row_dict[key]:
                    row_dict[key] = row_dict[key].strftime('%Y-%m-%d %H:%M:%S')
            result_list.append(row_dict)
        
        return Response(result_list)
    
class InsertarNewPhonoCondeza(generics.CreateAPIView):
    queryset = NewPhoneCondeza.objects.all()
    serializer_class = NewPhonoCondezaSerializer

class InsertarNewEmailCondeza(generics.CreateAPIView):
    queryset = NewEmailCondeza.objects.all()
    serializer_class = NewEmailCondezaSerializer

class ListarTipificacionesCondeza(generics.ListAPIView):
    queryset = CodigoRespuesta.objects.all()
    serializer_class = TipificacionCondezaSerializerReport

class ListarGestionesAllWallet(APIView):
    def get(self, request, tipo, rutdv):
        query = """
        WITH CombinedResults AS (
            SELECT 
                ac.fecha,
                ac.tipo,
                ac.respuesta,
                ac.telefono,
                ac.feccomp,
                ac.ruteje,
                ac.glosa
            FROM All_Contacts ac WITH (NOLOCK)
            LEFT JOIN Registro_Contacto rc WITH (NOLOCK) ON rc.rut = ac.rut
            WHERE rc.rut = %s

            UNION ALL

            SELECT 
                rc.fecha,
                t.tipo,
                t.GLOSA_ESTADO,
                rc.telefono,
                rc.feccomp,
                rc.ruteje,
                rc.glosa
            FROM Registro_Contacto rc WITH (NOLOCK)
            INNER JOIN report00.dbo.Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
            WHERE rc.rut = %s AND
            CAST(rc.fecha AS DATE) = CAST(GETDATE() AS DATE)
        ),
        OrderedResults AS (
            SELECT 
                cr.fecha,
                cr.tipo,
                cr.respuesta,
                cr.telefono,
                cr.feccomp,
                cr.ruteje,
                cr.glosa,
                nu.nombre,
                ROW_NUMBER() OVER (
                    PARTITION BY cr.fecha, cr.tipo, cr.respuesta, cr.telefono, 
                    cr.feccomp, cr.ruteje, cr.glosa 
                    ORDER BY cr.fecha DESC
                ) AS rn
            FROM CombinedResults cr
            LEFT JOIN report00.dbo.new_usuers nu ON cr.ruteje = nu.rut
        )
        SELECT TOP 15
            fecha,
            tipo,
            respuesta,
            telefono,
            feccomp,
            ruteje AS invalid,
            glosa,
            nombre AS ruteje
        FROM OrderedResults
        WHERE rn = 1
        ORDER BY fecha DESC;
        """

        # Selecciona la conexión basada en el parámetro tipo
        connection = connections[tipo]

        with connection.cursor() as cursor:
            cursor.execute(query, [rutdv, rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

        result_list = [dict(zip(columns, row)) for row in data]

        return Response(result_list)
    
class ListarGestionesAllWalletPass(APIView):
    def get(self, request, tipo, rutdv):
        query = """
        WITH CombinedResults AS (
            SELECT 
                ac.fecha,
                ac.tipo,
                ac.respuesta,
                ac.telefono,
                ac.feccomp,
                ac.ruteje,
                ac.glosa
            FROM All_Contacts ac WITH (NOLOCK)
            LEFT JOIN Registro_Contacto rc WITH (NOLOCK) ON rc.rut = ac.rut
            WHERE rc.rut = %s

            UNION ALL

            SELECT 
                rc.fecha,
                t.tipo,
                t.GLOSA_ESTADO,
                rc.telefono,
                rc.feccomp,
                rc.ruteje,
                rc.glosa
            FROM Registro_Contacto rc WITH (NOLOCK)
            INNER JOIN RPASS.dbo.Tipificaciones t WITH (NOLOCK) ON rc.idrespuesta = t.Idrespuesta
            WHERE rc.rut = %s AND
            CAST(rc.fecha AS DATE) = CAST(GETDATE() AS DATE)
        ),
        OrderedResults AS (
            SELECT 
                cr.fecha,
                cr.tipo,
                cr.respuesta,
                cr.telefono,
                cr.feccomp,
                cr.ruteje,
                cr.glosa,
                nu.nombre,
                ROW_NUMBER() OVER (
                    PARTITION BY cr.fecha, cr.tipo, cr.respuesta, cr.telefono, 
                    cr.feccomp, cr.ruteje, cr.glosa 
                    ORDER BY cr.fecha DESC
                ) AS rn
            FROM CombinedResults cr
            LEFT JOIN report00.dbo.new_usuers nu WITH (NOLOCK) ON cr.ruteje = nu.rut
        )
        SELECT TOP 15
            fecha,
            tipo,
            respuesta,
            telefono,
            feccomp,
            ruteje AS invalid,
            glosa,
            nombre AS ruteje
        FROM OrderedResults
        WHERE rn = 1
        ORDER BY fecha DESC;
        """

        # Selecciona la conexión basada en el parámetro tipo
        connection = connections[tipo]

        with connection.cursor() as cursor:
            cursor.execute(query, [rutdv, rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

        result_list = [dict(zip(columns, row)) for row in data]

        return Response(result_list)

#generals diary
class GetDataDiaryAPIView(APIView): 
    def get(self, request, tipo, ruteje, idclient):

        prefix = tipo.upper()
        
        # Verificar que los parámetros requeridos estén presentes
        if not ruteje or not tipo:
            return Response({"error": "Los parámetros 'ruteje' y 'tipo' son requeridos"}, status=400)
        
        # Construir la consulta SQL
        query = f'''
        WITH GestionesDelDia AS (
            SELECT 
                rc.Rut,
                rc.Ruteje,
                rc.Fecha_Gestion,
                rc.Fecha_Agenda,
                rc.Prefix,
                rc.telefono,
                rc.monto,
                CAST(rc.glosa AS VARCHAR(MAX)) AS glosa,
                rc.link,
                rcon.idrespuesta,
                ROW_NUMBER() OVER (PARTITION BY rc.Rut, CONVERT(date, rcon.fecha) ORDER BY rcon.fecha DESC) AS rn
            FROM 
                STORAGE.dbo.Volver_Llamar rc WITH (NOLOCK)
            INNER JOIN 
                {prefix}.dbo.Registro_Contacto rcon WITH (NOLOCK) ON rc.Rut = rcon.rut
        )
        SELECT DISTINCT 
            gd.Rut,
            gd.Ruteje,
            gd.Fecha_Gestion,
            gd.Fecha_Agenda,
            gd.Prefix,
            gd.telefono,
            gd.monto,
            gd.glosa,
            gd.link,
            'VOLVER A LLAMAR' AS ESTADO
        FROM 
            GestionesDelDia gd
        INNER JOIN 
            Cartera ct WITH (NOLOCK) ON gd.Rut = ct.rutDV
        JOIN 
            report00.dbo.campaigns c WITH (NOLOCK) ON c.active = 1 AND c.idclient = %s
        WHERE 
            gd.rn = 1
            AND gd.idrespuesta = '5'
            AND CONVERT(date, gd.Fecha_Gestion) >= c.inicio
            AND gd.prefix = %s
            AND gd.Fecha_Agenda >= CAST(GETDATE() AS DATE)
            AND gd.Ruteje = %s
        '''
        
        try:
            # Usar la conexión de la base de datos según el parámetro 'tipo'
            with connections[tipo].cursor() as cursor:
                cursor.execute(query, [idclient, prefix, ruteje])
                rows = cursor.fetchall()
        except DatabaseError as e:
            return Response({"error": str(e)}, status=500)
        
        # Definir las columnas para la respuesta
        columns = [
            'rut', 'ruteje', 'Fecha_Gestion', 'Fecha_Agenda', 'prefix', 'telefono',
            'monto', 'glosa', 'link', 'Estado'
        ]
        
        # Convertir los resultados a una lista de diccionarios
        results = [dict(zip(columns, row)) for row in rows]

        return Response(results, status=200)
    
     
     
class DiaryAllWallet(APIView):  
    def get(self, request, tipo, ruteje):
        # Verificar si el tipo de conexión existe en las bases de datos configuradas
        if tipo not in connections.databases:
            return JsonResponse({"error": "Tipo de conexión no válida"}, status=400)
        
        cursor = connections[tipo].cursor()
        try:
            # Nueva consulta con la lógica corregida
            query = """
            WITH LastRecord AS (
                SELECT 
                    rc.id, 
                    rc.rut AS rutgeneral, 
                    rc.fecha AS lastDate,
                    rc.glosa AS glosageneral,
                    ROW_NUMBER() OVER (PARTITION BY rc.rut ORDER BY rc.fecha DESC) AS RowNum
                FROM Registro_Contacto rc
                inner join Cartera c on c.RutDV = rc.rut
                WHERE CONVERT(date,fecha) >= CONVERT(date, GETDATE()) and CONVERT(date,fecha) <= DATEADD(DAY, 7, GETDATE())
            )
            SELECT 
                lr.rutgeneral, 
                rc.idrespuesta,
                lr.glosageneral,
                rc.Ruteje,
                rc.monto,
                vl.Fecha_Gestion,
                vl.Fecha_Agenda,
                rc.feccomp,
                rc.telefono,
                rc.modo,
                vl.link,
                rc.fecha,
                t.GLOSA_ESTADO,
                al.autorizaDate
            FROM LastRecord lr
            INNER JOIN Registro_Contacto rc ON lr.id = rc.id
            INNER JOIN report00.dbo.Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
            LEFT JOIN STORAGE.dbo.Volver_Llamar vl ON rc.fecha = vl.Fecha_Gestion
            LEFT JOIN STORAGE.dbo.AutorizaLLamado al ON lr.lastDate = al.fecha
            WHERE lr.RowNum = 1 -- Tomar solo la última fila por RUT
              AND rc.ruteje = %s -- Siempre debe coincidir con el Ruteje
              AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si'); -- Condiciones adicionales
            """
            # Ejecutar la consulta con el parámetro proporcionado
            cursor.execute(query, [ruteje])
            
            # Obtener los nombres de las columnas y los datos
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        except DatabaseError as e:
            return JsonResponse({"error": f"Error en la base de datos: {str(e)}"}, status=500)
        finally:
            cursor.close()
        
        # Convertir los resultados a una lista de diccionarios
        result_list = [dict(zip(columns, row)) for row in data]
        
        # Validar si se encontraron datos
        if not result_list:
            return Response({"message": "No se encontraron registros para este RUT"}, status=200)
        
        return Response(result_list)

#delete see
class DiaryAllWalletPass(APIView):   
    def get(self, request, ruteje):
        if not ruteje:
            return Response({"error": "El parámetro 'ruteje' es requerido"}, status=400)
        
        cursor = connections['pass'].cursor()
        try:
            query = """
            WITH LastRecord AS (
                SELECT 
                    rc.id, 
                    rc.rut AS rutgeneral, 
                    rc.fecha AS lastDate,
                    rc.glosa AS glosageneral,
                    c.Mail1_Nativo as Email1,
					c.Mail2_Nativo as Email2,
					c.Mail3_Nativo as Email3,
					c.Mail1_Rnut as Email4,
					c.Mail2_Rnut as Email5,
					c.Mail3_Rnut as Email6,
                    ROW_NUMBER() OVER (PARTITION BY rc.rut ORDER BY rc.fecha DESC) AS RowNum
                FROM Registro_Contacto rc
                inner join Cartera c on c.customer_nid = rc.rut
                WHERE CONVERT(date,fecha) >= CONVERT(date, GETDATE()) and CONVERT(date,fecha) <= DATEADD(DAY, 7, GETDATE())
            )
            SELECT 
                lr.rutgeneral, 
                rc.idrespuesta,
                lr.glosageneral,
                rc.ruteje,
                rc.monto,
                vl.Fecha_Gestion,
                vl.Fecha_Agenda,
                rc.feccomp,
                rc.telefono,
                rc.modo,
                vl.link,
                rc.fecha,
                t.GLOSA_ESTADO,
                al.autorizaDate,
                Email1,
				Email2,
				Email3,
				Email4,
				Email5,
				Email6
            FROM LastRecord lr
            INNER JOIN Registro_Contacto rc ON lr.id = rc.id
            INNER JOIN Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
            LEFT JOIN STORAGE.dbo.Volver_Llamar vl ON rc.fecha = vl.Fecha_Gestion
            LEFT JOIN STORAGE.dbo.AutorizaLLamado al ON lr.lastDate = al.fecha
            WHERE lr.RowNum = 1 -- Tomar solo la última fila por RUT
              AND rc.ruteje = %s -- Coincide con el Ruteje
              AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si'); -- Condiciones adicionales
            """
            cursor.execute(query, [ruteje])
        
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        except DatabaseError as e:
            return JsonResponse({"error": f"Error en la base de datos: {str(e)}"}, status=500)
        finally:
            cursor.close()
        
        result_list = [dict(zip(columns, row)) for row in data]
        
        if not result_list:
            return Response({"message": "No se encontraron registros para este RUT"}, status=200)
        
        return Response(result_list)

 
    
class SmsStatusAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Extraer los parámetros enviados por Siptel
        msgid = request.data.get('msgid')
        status_sms = request.data.get('status')
        fecha = request.data.get('fecha')

        # Verificar que los parámetros no estén vacíos
        if not msgid or not status_sms or not fecha:
            return Response({"error": "Parámetros faltantes"}, status=status.HTTP_400_BAD_REQUEST)

        # Conectar a la base de datos y realizar el INSERT
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                INSERT INTO API.dbo.StatusSMS (msgid, status, fecha) 
                VALUES (%s, %s, %s)
            """, [msgid, status_sms, fecha])
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()

        # Retornar 'ACK' como lo solicita la API de Siptel
        return Response({"message": "ACK"}, status=status.HTTP_200_OK)
    
    


class InsertaCallAgain(generics.CreateAPIView):
    queryset = VolverLlamar.objects.all()
    serializer_class = InsertaCallAgain

@api_view(['GET'])
def CombinedPhonesView(request):
    idclient = request.GET.get('idclient')
    rut = request.GET.get('rut')
    database_name = request.GET.get('database_name')

    if not idclient or not rut or not database_name:
        return Response({"error": "Faltan parámetros idclient, rut o database_name"}, status=400)
    database_name = database_name.upper()

    with connections['storage'].cursor() as cursor:  
        cursor.execute("EXEC dbo.proc_ObtenerTelefonosPorRUT %s, %s, %s", [rut, idclient, database_name])
        rows = cursor.fetchall()

    results = [{'rut': row[0], 'telefono': row[1]} for row in rows]

    return Response(results)
 
class GetCallAgainAll(APIView):
    def get(self, request, prefix):
        cursor = connections['storage'].cursor()
        try:
            query = """
                SELECT
                    Rut,
                    Ruteje,
                    Fecha_Gestion,
                    Fecha_Agenda,
                    telefono,
                    monto,
                    glosa,
                    link
                FROM
                    Volver_Llamar WITH (NOLOCK)
                WHERE
                    Prefix = %s
                    AND CAST(Fecha_Agenda AS DATE) >= CAST(GETDATE() AS DATE)
            """
            cursor.execute(query, [prefix])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)
    
    
    
class SendSMSNG(APIView): 
    def post(self, request, *args, **kwargs):
        number = request.data.get('number')
        message = request.data.get('message')
        
        if not number or not message:
            return Response({"success": False, "error": "Los parámetros 'number' y 'message' son requeridos."}, status=400)
        
        if not number.startswith('56'):
            number = f'56{number}'  
        
        url = "https://api-ng.siptel.cl/api/sms-ng"
        
        payload = {
            'token': 'QzEtdU6NVOMgRWkPgA0N',  
            'sender': '56442360466',          
            'mensaje_sms': message,
            'destino': number,                
            'camp': 'SIPTEL-NUEVA-CAMP-PRUEBA',  
            'hora_inicial': '09:00:00',
            'hora_termino': '18:45:00',
            'dia_lu': '1',
            'dia_ma': '1',
            'dia_mi': '1',
            'dia_ju': '1',
            'dia_vi': '1',
            'dia_sa': '0',
            'dia_do': '0',
            'campo_add': '{"cod_interno": "75826"}'  # JSON con campos adicionales, opcional
        }

        try:
            response = requests.post(url, data=payload)

            if response.status_code == 200:
                resultado = response.json()
                if resultado.get('nro_error') == 0:
                    return Response({"success": True, "msg_id": resultado.get("msg_id")})
                else:
                    return Response({"success": False, "error": f"Error en el envío: {resultado.get('nro_error')} - {resultado.get('detalle_error')} "})
            else:
                return Response({"success": False, "error": f"Error HTTP: {response.status_code}"})
        except Exception as e:
            return Response({"success": False, "error": str(e)})
        
        
class NASAudioSearch(APIView): 
    def get(self, request):
        # Obtener el parámetro "number" de la solicitud GET
        search_number = request.GET.get('number')

        if not search_number:
            return Response({'ok': False, 'error': 'El parámetro "number" es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # Configuración del NAS
        server = "192.168.5.10"
        share = "respaldo_KON3CTADOS"
        username = "kon3ctados"
        password = "icxnas2024"
        client_machine_name = "my_client"
        server_name = "my_server"
        remote_folder = "audios_respaldo_celulares_especialistas"
        
        # Crear conexión SMB
        conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)

        try:
            # Intentar conectar al NAS en el puerto 445
            assert conn.connect(server, 445)
        except Exception as e:
            return Response({'ok': False, 'error': f'Error al conectar al NAS: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Listar los archivos en el directorio remoto
            files = conn.listPath(share, remote_folder)

            # Imprimir los archivos para depuración
            for f in files:
                print(f"Archivo encontrado: {f.filename}")

            # Buscar archivos que contengan el número en el nombre
            matching_files = [f.filename for f in files if search_number in f.filename]

            if not matching_files:
                return Response({'ok': False, 'error': 'No se encontraron archivos que coincidan con el número'}, status=status.HTTP_404_NOT_FOUND)

            # Retornar los nombres de los archivos encontrados
            return Response({'ok': True, 'files': matching_files}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Cerrar la conexión al NAS
            conn.close()


class NASAudioSearchAll(APIView):  
    def get(self, request):
        # Obtener el parámetro "number" de la solicitud GET
        search_number = request.GET.get('number')

        if not search_number:
            return Response({'ok': False, 'error': 'El parámetro "number" es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # Configuración del NAS
        server = "192.168.5.10"
        share = "grabaciones_audios"
        username = "kon3ctados"
        password = "icxnas2024"
        client_machine_name = "my_client"
        server_name = "192.168.5.10"

        # Crear la conexión SMB
        conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)

        try:
            # Intentar conectar al NAS en el puerto 445
            if not conn.connect(server, 445):
                return Response({'ok': False, 'error': 'No se pudo conectar al NAS.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'ok': False, 'error': f'Error al conectar al NAS: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        matching_files = []
        page_size = 1000  # Número de archivos por "página"
        offset = 0

        try:
            while True:
                # Obtener una "página" de archivos desde el NAS
                files = conn.listPath(share, "", offset, page_size)

                # Verificar si "files" es una lista para evitar errores
                if not isinstance(files, list) or len(files) == 0:
                    break  # No hay más archivos para listar

                # Filtrar los archivos en esta página que contengan el `search_number`
                for f in files:
                    if search_number in f.filename:  # Buscar coincidencia en el nombre del archivo
                        matching_files.append(f.filename)

                offset += page_size  # Avanzar al siguiente conjunto de archivos

                # Salir si ya encontramos suficientes resultados
                if len(matching_files) >= 100:  # Limitar a 100 resultados
                    break

            if not matching_files:
                return Response({'ok': False, 'error': 'No se encontraron archivos que coincidan con el número'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'ok': True, 'files': matching_files}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Cerrar la conexión al NAS
            conn.close()
            
            
            

class NASAudioDownload(APIView): 
    def get(self, request):
        # Obtener el parámetro "filename" de la solicitud GET
        filename = request.GET.get('filename')

        if not filename:
            return Response({'ok': False, 'error': 'El parámetro "filename" es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # Configuración del NAS
        server = "192.168.5.10"
        share = "respaldo_KON3CTADOS"
        username = "kon3ctados"
        password = "icxnas2024"
        client_machine_name = "my_client"
        server_name = "my_server"
        remote_folder = "audios_respaldo_celulares_especialistas"
        
        # Crear conexión SMB
        conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)

        try:
            # Intentar conectar al NAS en el puerto 445
            assert conn.connect(server, 445)
        except Exception as e:
            return Response({'ok': False, 'error': f'Error al conectar al NAS: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Verificar si el archivo existe en el directorio remoto
            file_path = f"{remote_folder}/{filename}"

            # Crear un buffer en memoria para almacenar el archivo
            file_obj = BytesIO()

            # Descargar el archivo desde el NAS y almacenarlo en el buffer
            conn.retrieveFile(share, file_path, file_obj)

            # Colocar el puntero del buffer al principio
            file_obj.seek(0)

            # Crear la respuesta HTTP con el archivo para su descarga
            response = HttpResponse(file_obj, content_type='audio/wav')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return Response({'ok': False, 'error': f'Error al descargar el archivo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Cerrar la conexión al NAS
            conn.close()
            
        
#pass
class ConsultaRutViewPass(APIView):
    def get(self, request, rutdv):
        cursor = connections['pass'].cursor()
        try:
            cursor.execute("""
                SELECT
        ct.rutDV AS RUT,
         
                    MAX(ct.boletas) AS BOLETAS,
                    MAX(ct.monto) AS MONTO,
                    MAX(c.customer_name) AS NOMBRE,
                    MAX(c.Mail1_Nativo) AS EMAIL1,
					MAX(c.Mail2_Nativo) AS EMAIL2,
					MAX(c.Mail3_Nativo) AS EMAI3,
					MAX(c.Mail1_Rnut) AS EMAIL4,
					MAX(c.Mail2_Rnut) AS EMAIL5,
					MAX(c.Mail3_Rnut) AS EMAIl6,
                    MAX(c.Comuna) AS COMUNA,
                    MAX(c.Región) AS Region,
                    MAX(c.Direccion) AS direccion,
                    max(c.Fono1_Nativo) AS fono1,
					max(c.Fono2_Nativo) AS fono2,
					max(c.Fono3_Nativo) AS fono3,
					max(c.Fono1_Rnut) AS fono4,
					max(c.Fono2_Rnut) AS fono5,
					max(c.Fono3_Rnut) AS fono6,
                    max(c.Cesion) AS cesion        
                FROM 
                    Cartera_Totales ct WITH (NOLOCK)
                JOIN 
                    Cartera c WITH (NOLOCK) ON ct.rutDV = c.customer_nid
                WHERE 
                    c.customer_nid = %s
                GROUP BY 
                    ct.rutDV
            """, [rutdv])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    
class InsertarRegistroContactoPass(generics.CreateAPIView):
    queryset = RegistroContactoPass.objects.all()
    serializer_class = RegistroContactoPassSerializer

class ContactByRUTPass(APIView):
    def get(self, request, customer_nid):
        contacts = CarteraPass.objects.filter(customer_nid = customer_nid)  
        serializer = CarteraPassSerializer(contacts, many=True)
        return Response(serializer.data)
    
class InsertarNewPhonoPass(generics.CreateAPIView):
    queryset = NewPhonePass.objects.all()
    serializer_class = NewPhonoPassSerializer

class InsertarNewEmailPass(generics.CreateAPIView):
    queryset = NewEmailPass.objects.all()
    serializer_class = NewEmailPassSerializer
       
class TipificacionesAll(APIView):
    def get(self, request):
        try:
            with connections['pass'].cursor() as cursor:
                cursor.execute("SELECT * FROM Tipificaciones")
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
            result_list = [dict(zip(columns, row)) for row in data]
            return Response(result_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RefinanciacionesPass(APIView):
    def get(self, request, rut):
        cursor = connections['pass'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM Refinanciaciones WITH (NOLOCK) WHERE CustomerNid = %s
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    
    
class DescuentoPass(APIView):
    def get(self, request, rut):
        cursor = connections['pass'].cursor()
        try:
            cursor.execute("""
                SELECT MONTO_DESC AS descuento_total, Saldo_Total as deuda_total, PORC_DESC as porcentaje, VALOR_A_PAGAR AS pagar FROM Descuento_Old WITH (NOLOCK) WHERE Rut = %s
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

      
        result_list = [dict(zip(columns, row)) for row in data]
        
        return Response(result_list)
    
class Refinanciaciones(APIView):
    def get(self, request, rut):
        cursor = connections['pass'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM Refinanciaciones WHERE CustomerNid = %s
            """, [rut])
            data = cursor.fetchall()
        finally:
            cursor.close()
        has_data = bool(data) 
        return Response({has_data})
    
class DescuentoAllWallet(APIView): 
    def get(self, request, tipo, rut):
        if tipo not in connections.databases:
            return JsonResponse({"error": "Tipo de conexión no válida"}, status=400)
        
        cursor = connections[tipo].cursor()
        try:
            if tipo == 'acsa':
                cursor.execute("""
                    SELECT descuento_total FROM  vw_descuento_new  WITH (NOLOCK) WHERE rut = %s
                """, [rut])
            elif tipo == 'avo':
                cursor.execute("""
                    SELECT SUM(Monto) AS MontoReal, SUM(Descuento) AS descuento, SUM(MontoaPagar) AS allPaid 
                    FROM AVO.dbo.Descuento WITH (NOLOCK) WHERE RutDV = %s
                """, [rut])
            else:
                cursor.execute("""
                    SELECT * FROM Descuento WITH (NOLOCK) WHERE RutDV = %s
                """, [rut])
            
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        finally:
            cursor.close()

        result_list = [dict(zip(columns, row)) for row in data]
        
        if not result_list:
            return Response({"message": "No se encontraron descuentos para este RUT"}, status=404)
        
        return Response(result_list)
    

class SendMailingView(APIView):
    def post(self, request, *args, **kwargs):
        recipient_email = request.data.get('email')
        subject = request.data.get('subject', 'Sin Asunto')  # Si no se proporciona, usar 'Sin Asunto'
        html_content = request.data.get('body')  # Asegúrate de que el `body` sea un texto HTML
        if not recipient_email or not html_content:
            return Response({"success": False, "error": "Los campos 'email' y 'body' son requeridos y 'body' debe ser texto HTML."}, status=400)
        try:
            text_content = strip_tags(html_content)  
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,  
                to=[recipient_email]
            )
            email.attach_alternative(html_content, "text/html")
            if request.FILES:
                for file_key in request.FILES:
                    uploaded_file = request.FILES[file_key]
                    if isinstance(uploaded_file, InMemoryUploadedFile):
                        email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
            email.send()
            return Response({"success": True, "message": "Correo enviado correctamente con adjuntos."}, status=200)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)

class InsertarRegistroContactoAutorizaLlamado(generics.CreateAPIView):
    queryset = RegistroContactoAutoriza.objects.all()
    serializer_class = RegistroContactoAutorizaLLamadoSerializer
    
    
class getCallAutorizados(APIView):
    def get(self, request, ruteje, tipo):
        query = """
            SELECT * FROM [STORAGE].[dbo].[AutorizaLLamado]
            WHERE ruteje = %s AND prefix = %s
        """
        try:
            with connections['storage'].cursor() as cursor:
                cursor.execute(query, [ruteje, tipo])
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
            
            if not data:
                return Response({'message': 'No se encontraron registros.'}, status=404)
            
            result_list = [dict(zip(columns, row)) for row in data]
            return Response(result_list)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)
  
  

# insert all wallet email phono      
class InsertPhonoAllWallets(APIView):
    def post(self, request, *args, **kwargs):
        tipo = request.data.get('tipo')
        rut = request.data.get('rut')
        ruteje = request.data.get('ruteje')
        telefono = request.data.get('telefono')
        fecha = request.data.get('fecha')

        cursor = connections[tipo].cursor()
        try:
            # Ejecución de la consulta SQL
            cursor.execute("""
                INSERT INTO New_Phone (rut, ruteje, telefono, fecha)
                VALUES (%s, %s, %s, %s)
            """, [rut, ruteje, telefono, fecha])
            
            # Confirmación del éxito de la inserción
            return Response({"message": "Data inserted successfully"}, status=201)
        except Exception as e:
            # Manejo de errores
            return Response({"error": str(e)}, status=400)
        finally:
            # Cierre del cursor
            cursor.close()

class InsertEmailAllWallets(APIView):
    def post(self, request, *args, **kwargs):
        tipo = request.data.get('tipo')
        rut = request.data.get('rut')
        ruteje = request.data.get('ruteje')
        telefono = request.data.get('email')
        fecha = request.data.get('fecha')

        cursor = connections[tipo].cursor()
        try:
            # Ejecución de la consulta SQL
            cursor.execute("""
                INSERT INTO New_Email (rut, ruteje, email, fecha)
                VALUES (%s, %s, %s, %s)
            """, [rut, ruteje, telefono, fecha])
            
            # Confirmación del éxito de la inserción
            return Response({"message": "Data inserted successfully"}, status=201)
        except Exception as e:
            # Manejo de errores
            return Response({"error": str(e)}, status=400)
        finally:
            # Cierre del cursor
            cursor.close()
            
class InsertDireccionWalletSvia(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data.get('id')  # puede venir como None o vacío
        rut = request.data.get('rut')
        direccion = request.data.get('direccion')
        comuna = request.data.get('comuna')
        active = request.data.get('active')
        ruteje = request.data.get('ruteje')
        fecha = request.data.get('fecha')

        # Aseguramos que id sea None si viene vacío
        id = None if not id else id

        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                EXEC sp_GuardarDireccionSvia 
                    @id = %s,
                    @rut = %s,
                    @direccion = %s,
                    @comuna = %s,
                    @active = %s,
                    @ruteje = %s,
                    @fecha = %s
            """, [id, rut, direccion, comuna, active, ruteje, fecha])

            return Response({"message": "Procedimiento ejecutado correctamente"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        finally:
            cursor.close()
  
#get all client metadata        
class getAllEmailClient(APIView):
    def get(self, request, tipo, rut):
        # Verificar si los parámetros 'tipo' y 'rut' son válidos
        if not tipo or not rut:
            return Response({"error": "Missing 'tipo' or 'rut' parameter"}, status=400)
        
        cursor = connections[tipo].cursor()
        try:
            cursor.execute("""
                SELECT * FROM New_Email WITH (NOLOCK) WHERE rut = %s
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            
            if not data:
                return Response({"message": "No records found"}, status=200)
                
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()

        # Crear el resultado a partir de los datos obtenidos
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)

class getAllDirecionClientSvia(APIView):
    def get(self, request, rut):
        # Verificar si los parámetros 'tipo' y 'rut' son válidos
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM New_Direccion WITH (NOLOCK) WHERE Rut = %s
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            
            if not data:
                return Response({"message": "No records found"}, status=200)
                
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()

        # Crear el resultado a partir de los datos obtenidos
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)

class getDescuentoSvia(APIView): 
    def get(self, request, rut):
        cursor = connections['svia'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM SVIA.dbo.Descuento WITH (NOLOCK) WHERE Rut = %s
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)


class getAllPhoneClient(APIView):
    def get(self, request, tipo, rut):
        # Verificar si los parámetros 'tipo' y 'rut' son válidos
        if not tipo or not rut:
            return Response({"error": "Missing 'tipo' or 'rut' parameter"}, status=400)
        
        cursor = connections[tipo].cursor()
        try:
            cursor.execute("""
                SELECT * FROM New_Phone WITH (NOLOCK) WHERE rut = %s
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            
            if not data:
                return Response({"message": "No records found"}, status=200)
                
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()

        # Crear el resultado a partir de los datos obtenidos
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)


#sort all user wallet 
class getUsersPassWallet(APIView):
    def get(self, request, idclient):
        with connections['pass'].cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT rc.ruteje, us.NameUser
                FROM [dbo].[Registro_Contacto] rc
                INNER JOIN [report00].[dbo].[campaigns] c
                    ON c.active = 1 AND c.idclient = %s
                INNER JOIN [192.168.5.18].API.dbo.Users us
                    ON rc.ruteje = us.Rut
                WHERE CONVERT(date, rc.fecha) >= c.inicio 
                AND CONVERT(date, rc.fecha) <= c.termino
            """, [idclient])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)
   
#show all wallet client 
class getUsersAllWallet(APIView):
    def get(self, request, tipo, idclient):
        if not idclient or not tipo:
            return Response({"error": "Parámetros inválidos"}, status=400)

        try:
            with connections[tipo].cursor() as cursor:
                query = """
                    SELECT DISTINCT rc.ruteje, us.nombre
                    FROM [dbo].[Registro_Contacto] rc
                    INNER JOIN [report00].[dbo].[campaigns] c
                        ON c.active = 1 AND c.idclient = %s
                    INNER JOIN report00.dbo.new_usuers us
                        ON rc.ruteje = us.rut
                    WHERE rc.fecha BETWEEN c.inicio AND c.termino
                """
                cursor.execute(query, [idclient])
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

            if not data:
                return Response({"message": "No se encontraron registros"}, status=404)

            result_list = [dict(zip(columns, row)) for row in data]
            return Response(result_list)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


#show compromiso por cada ejecutivo  revisar estooo lo mas problable 
class showCdToSupervision(APIView):
    def get(self, request, tipo, ruteje):
        # Validar tipo de conexión
        if tipo not in connections.databases:
            return JsonResponse({"error": "Tipo de conexión no válido"}, status=400)

        # Validar parámetro ruteje
        if not ruteje:
            return JsonResponse({"error": "El parámetro 'ruteje' es obligatorio"}, status=400)

        # Consulta SQL optimizada
        query = """
        ;WITH LastRecord AS (
            SELECT 
                rc.id, 
                rc.rut AS rutgeneral, 
                rc.fecha AS lastDate,
                rc.glosa AS glosageneral,
                ROW_NUMBER() OVER (PARTITION BY rc.rut ORDER BY rc.fecha DESC) AS RowNum
            FROM Registro_Contacto rc
            INNER JOIN Cartera c ON c.RutDV = rc.rut
            WHERE CONVERT(DATE, rc.fecha) 
                  BETWEEN DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0) 
                      AND DATEADD(DAY, 5, GETDATE())
        )
        SELECT 
            lr.rutgeneral, 
            rc.idrespuesta,
            lr.glosageneral,
            rc.Ruteje,
            rc.monto,
            vl.Fecha_Gestion,
            vl.Fecha_Agenda,
            rc.feccomp,
            rc.telefono,
            rc.modo,
            vl.link,
            rc.fecha,
            t.GLOSA_ESTADO,
            al.autorizaDate
        FROM LastRecord lr
        INNER JOIN Registro_Contacto rc 
            ON lr.id = rc.id
        INNER JOIN report00.dbo.Tipificaciones t 
            ON rc.idrespuesta = t.Idrespuesta
        LEFT JOIN STORAGE.dbo.Volver_Llamar vl 
            ON rc.fecha = vl.Fecha_Gestion
        LEFT JOIN STORAGE.dbo.AutorizaLLamado al 
            ON lr.lastDate = al.fecha
        WHERE lr.RowNum = 1 
          AND rc.ruteje = %s  
          AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si')
        ORDER BY rc.fecha DESC;
        """

        # Ejecutar consulta y procesar resultados
        try:
            with connections[tipo].cursor() as cursor:
                cursor.execute(query, [ruteje])
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
        except DatabaseError as e:
            return JsonResponse({"error": f"Error en la base de datos: {str(e)}"}, status=500)

        # Convertir resultados en lista de diccionarios
        result_list = [dict(zip(columns, row)) for row in data]

        # Validar si hay datos encontrados
        if not result_list:
            return Response({"message": "No se encontraron registros para este RUT"}, status=200)

        return Response(result_list, status=200)


#revisar lo mas problable
class showCdToSupervisionPass(APIView):
    def get(self, request, ruteje):
        # Validar parámetro ruteje
        if not ruteje:
            return JsonResponse({"error": "El parámetro 'ruteje' es obligatorio"}, status=400)
        
        # Consulta SQL con la lógica corregida
        query = """
        WITH LastRecord AS (
            SELECT 
                rc.id, 
                rc.rut AS rutgeneral, 
                rc.fecha AS lastDate,
                rc.glosa AS glosageneral,
                ROW_NUMBER() OVER (PARTITION BY rc.rut ORDER BY rc.fecha DESC) AS RowNum
            FROM Registro_Contacto rc
            inner join Cartera c on c.customer_nid = rc.rut
            WHERE CONVERT(date, fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)
              AND CONVERT(date, fecha) <= DATEADD(DAY, 5, GETDATE())
        )
        SELECT 
            lr.rutgeneral, 
            rc.idrespuesta,
            lr.glosageneral,
            rc.Ruteje,
            rc.monto,
            vl.Fecha_Gestion,
            vl.Fecha_Agenda,
            rc.feccomp,
            rc.telefono,
            rc.modo,
            vl.link,
            rc.fecha,
            t.GLOSA_ESTADO,
            al.autorizaDate
        FROM LastRecord lr
        INNER JOIN Registro_Contacto rc ON lr.id = rc.id
        INNER JOIN report00.dbo.Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
        LEFT JOIN STORAGE.dbo.Volver_Llamar vl ON rc.fecha = vl.Fecha_Gestion
        LEFT JOIN STORAGE.dbo.AutorizaLLamado al ON lr.lastDate = al.fecha
        WHERE lr.RowNum = 1 -- Tomar solo la última fila por RUT
          AND rc.ruteje = %s -- Coincidir con el Ruteje
          AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si'); -- Condiciones adicionales
        """
        
        # Ejecutar consulta y procesar resultados
        try:
            with connections['pass'].cursor() as cursor:
                cursor.execute(query, [ruteje])
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
        except DatabaseError as e:
            return JsonResponse({"error": f"Error en la base de datos: {str(e)}"}, status=500)

        # Convertir los resultados en una lista de diccionarios
        result_list = [dict(zip(columns, row)) for row in data]
        
        # Validar si se encontraron datos
        if not result_list:
            return Response({"message": "No se encontraron registros para este RUT"}, status=200)
        
        return Response(result_list, status=200)

#ok gestiones de compromisos Rotos
class getGestionRutWallets(APIView):
    def get(self, request,dbName, rut):
        query_pass = """
                SELECT 
                    rc.rut,
                    rc.monto,
                    rc.ruteje,
                    nu.nombre,
                    rc.fecha,
                    rc.feccomp,
                    vl.Fecha_Agenda,
                    al.autorizaDate,
                    rc.glosa,
                    t.GLOSA_ESTADO,
                    rc.glosa
                FROM Registro_Contacto rc
                INNER JOIN report00.dbo.new_usuers nu ON rc.ruteje = nu.rut
                INNER JOIN Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
                LEFT JOIN STORAGE.dbo.Volver_Llamar vl ON rc.fecha = vl.Fecha_Gestion
                LEFT JOIN STORAGE.dbo.AutorizaLLamado al ON rc.fecha = al.fecha
                WHERE rc.rut = %s 
                AND (CONVERT(date, rc.fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0) 
                     AND CONVERT(date, rc.fecha) <= DATEADD(DAY, 7, GETDATE()))
            """
            
        query_otros = """
            SELECT 
                 rc.rut,
			    nu.nombre,
			    rc.telefono,
				rc.feccomp,
				 vl.Fecha_Agenda as Fecha_Llamar,
                al.autorizaDate as Autorizo_Llamado, 
                rc.monto,
                rc.ruteje,
                rc.fecha as Fecha_Gestion ,
                rc.glosa,
                t.GLOSA_ESTADO as Tipificacion
            FROM Registro_Contacto rc
            INNER JOIN report00.dbo.new_usuers nu ON rc.ruteje = nu.rut
            INNER JOIN report00.dbo.Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
            LEFT JOIN STORAGE.dbo.Volver_Llamar vl ON rc.fecha = vl.Fecha_Gestion
            LEFT JOIN STORAGE.dbo.AutorizaLLamado al ON rc.fecha = al.fecha
            WHERE rc.rut = %s 
            AND (CONVERT(date, rc.fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0) 
                 AND CONVERT(date, rc.fecha) <= DATEADD(DAY, 7, GETDATE()))
        """
        query = query_pass if dbName == 'pass' else query_otros
        
        try:
            with connections[dbName].cursor() as cursor:
                cursor.execute(query, [rut])
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
            
            if not data:
                return Response({'message': 'No se encontraron registros.'}, status=404)
            
            result_list = [dict(zip(columns, row)) for row in data]
            return Response(result_list)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    
    
   
  
#wallet svia dicom   
class dicomSvia(APIView):
    def get(self, request, rut):
        cursor = connections['svia'].cursor()
        try:
            cursor.execute("""
                select * from Dicom where RutDV = %s
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Cerrar el cursor correctamente
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
        
#monedero for all wallet BIENN
class CompromisosRotosAllWallet(APIView):  
    def get(self, request,tipo):
        with connections[tipo].cursor() as cursor:
            try:
                cursor.execute("""
                    WITH CTE AS (
                        SELECT 
                            rc.id AS RegistroId,
                            c.id AS CarteraId,
                            rc.rut,       
                            rc.idrespuesta,
                            rc.fecha AS fechaGestion,
                            rc.feccomp,
                            c.RutDV,
                            al.fecha AS fechaGestionAutorizo,
                            al.autorizaDate,
                            vl.Fecha_Agenda,
                            vl.Fecha_Gestion,
                            rc.monto,
                            rc.telefono,
                            ROW_NUMBER() OVER (PARTITION BY rc.id, rc.rut ORDER BY rc.fecha DESC) AS RowNum
                        FROM 
                            Registro_Contacto rc
                        INNER JOIN 
                            Cartera c 
                            ON c.RutDV = rc.rut
                        LEFT JOIN 
                            STORAGE.dbo.Volver_Llamar vl 
                            ON rc.fecha = vl.Fecha_Gestion -- Relación por RUT
                        LEFT JOIN 
                            STORAGE.dbo.AutorizaLLamado al 
                            ON rc.fecha = al.fecha -- Relación por RUT
                        WHERE 
                            CONVERT(date, rc.fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0) 
                            AND CONVERT(date, rc.fecha) <= DATEADD(DAY, 7, GETDATE())
                            AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si')
                    )
                    SELECT 
                        RegistroId,
                        CarteraId,
                        rut,       
                        idrespuesta,
                        fechaGestion,
                        feccomp,
                        RutDV,
                        fechaGestionAutorizo,
                        autorizaDate,
                        Fecha_Agenda,
                        Fecha_Gestion,
                        monto,
                        telefono
                    FROM CTE
                    WHERE RowNum = 1;
                """)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not data:
            return Response({'message': 'No se encontraron registros.'}, status=status.HTTP_204_NO_CONTENT)
        
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
 
 
 
 
 
#all compromisos rotos de los ejecutivos  BIENN 
class CompromisosRotosPass(APIView):   
    def get(self, request):
        with connections['pass'].cursor() as cursor:
            try:
                cursor.execute("""
                    WITH CTE AS (
                        SELECT 
                            rc.id AS RegistroId,
                            c.id AS CarteraId,
                            nu.nombre,       
                            rc.idrespuesta,
                            rc.fecha AS fechaGestion,
                            rc.feccomp,
                            c.customer_nid,
                            al.fecha AS fechaGestionAutorizo,
                            al.autorizaDate,
                            vl.Fecha_Agenda,
                            vl.Fecha_Gestion,
                            rc.monto,
                            ROW_NUMBER() OVER (PARTITION BY rc.rut ORDER BY rc.fecha DESC) AS RowNum
                        FROM 
                            Registro_Contacto rc
                        INNER JOIN 
                            Cartera c 
                            ON c.customer_nid = rc.rut
                            inner join report00.dbo.new_usuers nu
                            on rc.ruteje = nu.rut
                        LEFT JOIN 
                            STORAGE.dbo.Volver_Llamar vl 
                            ON rc.fecha = vl.Fecha_Gestion -- Relación por RUT
                        LEFT JOIN 
                            STORAGE.dbo.AutorizaLLamado al 
                            ON rc.fecha = al.fecha -- Relación por RUT
                        WHERE 
                            CONVERT(date, rc.fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0) 
                            AND CONVERT(date, rc.fecha) <= DATEADD(DAY, 7, GETDATE())
                            AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si')
                    )
                    SELECT 
                        RegistroId,
                        CarteraId,      
                        idrespuesta,
                        fechaGestion,
                        feccomp,
                        customer_nid,
                        fechaGestionAutorizo,
                        autorizaDate,
                        Fecha_Agenda,
                        Fecha_Gestion,
                        monto,
                        nombre
                    FROM CTE
                    WHERE RowNum = 1;
                """)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not data:
            return Response({'message': 'No se encontraron registros.'}, status=status.HTTP_204_NO_CONTENT)
        
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)


#comprimisos rotos pass ejecutivas 
class CompromisosRotosEjecutivosPass(APIView):  
    def get(self, request, ruteje):
        with connections['pass'].cursor() as cursor:
            try:
                query = """
                    WITH CTE AS ( 
                        SELECT 
                            rc.id AS RegistroId,
                            c.id AS CarteraId,
                            rc.rut,       
                            rc.idrespuesta,
                            rc.fecha AS fechaGestion,
                            rc.feccomp,
                            c.customer_nid,
                            al.fecha AS fechaGestionAutorizo,
                            al.autorizaDate,
                            vl.Fecha_Agenda,
                            vl.Fecha_Gestion,
                            rc.monto,
                            rc.ruteje,
                            ROW_NUMBER() OVER (
                                PARTITION BY rc.rut 
                                ORDER BY rc.fecha DESC
                            ) AS RowNum
                        FROM 
                            Registro_Contacto rc
                        INNER JOIN 
                            Cartera c ON c.customer_nid = rc.rut
                        LEFT JOIN 
                            STORAGE.dbo.Volver_Llamar vl ON rc.fecha = vl.Fecha_Gestion
                        LEFT JOIN 
                            STORAGE.dbo.AutorizaLLamado al ON rc.fecha = al.fecha
                        WHERE 
                            CONVERT(date, rc.fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0) 
                            AND CONVERT(date, rc.fecha) <= DATEADD(DAY, 7, GETDATE())
                            AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si')
                    )
                    SELECT 
                        RegistroId,
                        CarteraId,
                        rut,       
                        idrespuesta,
                        fechaGestion,
                        feccomp,
                        customer_nid,
                        fechaGestionAutorizo,
                        autorizaDate,
                        Fecha_Agenda,
                        Fecha_Gestion,
                        monto,
                        ruteje
                    FROM CTE
                    WHERE RowNum = 1 
                      AND ruteje = %s
                """  # Utiliza %s para la parametrización
                cursor.execute(query, [ruteje])  # Pasa ruteje como parámetro
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
                
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not data:
            return Response({'message': 'No se encontraron registros.'}, status=status.HTTP_204_NO_CONTENT)
        
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
 
 
 
 
#REVISAR
class CompromisosRotosEjecutivoAllWallet(APIView):  
    def get(self, request,tipo,ruteje):
        with connections[tipo].cursor() as cursor:
            try:
                query="""
                    WITH CTE AS (
                        SELECT 
                            rc.id AS RegistroId,
                            c.id AS CarteraId,
                            rc.rut,       
                            rc.idrespuesta,
                            rc.fecha AS fechaGestion,
                            rc.feccomp,
                            c.RutDV,
                            al.fecha AS fechaGestionAutorizo,
                            al.autorizaDate,
                            vl.Fecha_Agenda,
                            vl.Fecha_Gestion,
                            rc.monto,
                            rc.ruteje,
                            ROW_NUMBER() OVER (PARTITION BY rc.id, rc.rut ORDER BY rc.fecha DESC) AS RowNum
                        FROM 
                            Registro_Contacto rc
                        INNER JOIN 
                            Cartera c 
                            ON c.RutDV = rc.rut
                        LEFT JOIN 
                            STORAGE.dbo.Volver_Llamar vl 
                            ON rc.fecha = vl.Fecha_Gestion -- Relación por RUT
                        LEFT JOIN 
                            STORAGE.dbo.AutorizaLLamado al 
                            ON rc.fecha = al.fecha -- Relación por RUT
                        WHERE 
                            CONVERT(date, rc.fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0) 
                            AND CONVERT(date, rc.fecha) <= DATEADD(DAY, 7, GETDATE())
                            AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si')
                    )
                    SELECT 
                        RegistroId,
                        CarteraId,
                        rut,       
                        idrespuesta,
                        fechaGestion,
                        feccomp,
                        RutDV,
                        fechaGestionAutorizo,
                        autorizaDate,
                        Fecha_Agenda,
                        Fecha_Gestion,
                        monto
                    FROM CTE
                    WHERE RowNum = 1
                     AND ruteje = %s
                    
                """
                cursor.execute(query,[ruteje])
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not data:
            return Response({'message': 'No se encontraron registros.'}, status=status.HTTP_204_NO_CONTENT)
        
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)   


#crm   for delete   
class MonederoAllWallet(APIView): 
    def get(self, request,tipo):
        with connections[tipo].cursor() as cursor:
            try:
                cursor.execute("""
                    WITH LastRecord AS (
                        SELECT 
                            rc.id, 
                            rc.idrespuesta,
                            rc.rut AS rutCliente, 
                            rc.fecha AS lastDate,
                            rc.ruteje,
                            rc.glosa AS glosageneral,
                            rc.feccomp,
                            rc.modo,
                            ROW_NUMBER() OVER (PARTITION BY rc.rut ORDER BY rc.fecha DESC) AS RowNum
                        FROM Registro_Contacto rc
                        INNER JOIN Cartera c ON rc.rut = c.RutDV
                        WHERE CONVERT(date, fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0) 
                              AND CONVERT(date, fecha) <= DATEADD(DAY, 5, GETDATE())
                    )
                    SELECT 
                        lr.idrespuesta, 
                        rutCliente, 
                        lastDate, 
                        glosageneral, 
                        nu.nombre, 
                        lr.feccomp, 
                        lr.modo,
                        lr.ruteje,
                        t.GLOSA_ESTADO 
                    FROM LastRecord lr
                    INNER JOIN report00.dbo.Tipificaciones t ON lr.idrespuesta = t.Idrespuesta
                    INNER JOIN report00.dbo.new_usuers nu ON lr.ruteje = nu.rut
                    WHERE RowNum = 1
                      AND t.GLOSA_GESTION = 'PAGO TOTAL'
                """)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
            except Exception as e:  # Captura la excepción específica si es posible
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not data:  # Validación para manejar datos vacíos
            return Response({'message': 'No se encontraron registros.'}, status=status.HTTP_204_NO_CONTENT)
        
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)        
    
#crm for delete
class AllWalleteMonedero(APIView):
    def get(self, request, tipo):
        # Verificar si la conexión existe
        if tipo not in connections:
            return Response({'error': 'Tipo de conexión inválido'}, status=400)

        with connections[tipo].cursor() as cursor:
            cursor.execute("""
                SELECT * 
                FROM Pagos p 
                INNER JOIN All_Contacts al 
                ON al.rut = p.rut
            """)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

        # Si no hay resultados en la consulta, devolver un mensaje con HTTP 200
        if not data:
            return Response({'message': 'No se encontraron datos disponibles'}, status=200)

        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)

#crm monedero de pagos
class PagosWallet(APIView):
    def get(self, request, tipo):
        cursor = connections[tipo].cursor()

        try:
            # Definimos la consulta según el tipo
            if tipo == 'acsa':
                query = """
                    SELECT COUNT(rut) AS Ruts, SUM(pago) AS Monto
                    FROM Pagos
                """
            elif tipo == 'avo':
                query = """
                    SELECT COUNT(RUTDV) AS Ruts, SUM(MontoPagado) AS Monto
                    FROM Pagos_Inf
                """
            elif tipo == 'pass':
                query = """
                    SELECT COUNT(rut) AS Ruts, SUM(Monto) AS Monto
                    FROM Pagos
                """
            elif tipo == 'global':
                query = """
                    SELECT COUNT(rut) AS Ruts, SUM(TotalComprobante) AS Monto
                    FROM Pagos
                """
            elif tipo == 'svia':
                query = """
                    SELECT COUNT(Rut) AS Ruts, SUM(Monto_Pago) AS Monto
                    FROM Pagos
                """
            else:
                return Response({'error': 'Tipo no válido'}, status=400)

            # Ejecutamos la consulta
            cursor.execute(query)
            
            # Obtenemos las columnas y los datos
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

            # Convertimos los resultados a una lista de diccionarios
            result_list = [dict(zip(columns, row)) for row in data]

        finally:
            # Cerramos el cursor
            cursor.close()

        # Devolvemos la respuesta
        return Response(result_list)
    
    
#compromisos de todo el mess ejecutivos
class TotalMontoCompromiso(APIView):
    def get(self, request, tipo):
        # Validación del tipo de conexión
        if tipo not in connections:
            return Response({'error': 'Tipo no válido'}, status=400)

        cursor = connections[tipo].cursor()

        try:
            # Definimos la consulta según el tipo
            if tipo == 'pass':
                query = """
                    WITH LastRecord AS (
                        SELECT 
                            rc.id, 
                            rc.rut AS rutgeneral, 
                            rc.fecha AS lastDate,
                            rc.glosa AS glosageneral,
                            ROW_NUMBER() OVER (PARTITION BY rc.rut ORDER BY rc.fecha DESC) AS RowNum
                        FROM Registro_Contacto rc
                        INNER JOIN Cartera c ON c.customer_nid = rc.rut
                        WHERE CONVERT(date, rc.fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)
                          AND CONVERT(date, rc.fecha) <= DATEADD(DAY, 5, GETDATE())
                    )
                    SELECT 
                        COUNT(DISTINCT lr.rutgeneral) AS TotalRuts,
                        SUM(rc.monto) AS TotalMonto
                    FROM LastRecord lr
                    INNER JOIN Registro_Contacto rc ON lr.id = rc.id
                    INNER JOIN report00.dbo.Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
                    LEFT JOIN STORAGE.dbo.Volver_Llamar vl ON rc.fecha = vl.Fecha_Gestion
                    LEFT JOIN STORAGE.dbo.AutorizaLLamado al ON lr.lastDate = al.fecha
                    WHERE lr.RowNum = 1
                      AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si');
                """
            else:  # Para cualquier otro tipo, incluido 'avo'
                query = """
                    WITH LastRecord AS (
                        SELECT 
                            rc.id, 
                            rc.rut AS rutgeneral, 
                            rc.fecha AS lastDate,
                            rc.glosa AS glosageneral,
                            ROW_NUMBER() OVER (PARTITION BY rc.rut ORDER BY rc.fecha DESC) AS RowNum
                        FROM Registro_Contacto rc
                        INNER JOIN Cartera c ON c.RutDV = rc.rut
                        WHERE CONVERT(date, rc.fecha) >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)
                          AND CONVERT(date, rc.fecha) <= DATEADD(DAY, 5, GETDATE())
                    )
                    SELECT 
                        COUNT(DISTINCT lr.rutgeneral) AS TotalRuts,
                        SUM(rc.monto) AS TotalMonto
                    FROM LastRecord lr
                    INNER JOIN Registro_Contacto rc ON lr.id = rc.id
                    INNER JOIN report00.dbo.Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
                    LEFT JOIN STORAGE.dbo.Volver_Llamar vl ON rc.fecha = vl.Fecha_Gestion
                    LEFT JOIN STORAGE.dbo.AutorizaLLamado al ON lr.lastDate = al.fecha
                    WHERE lr.RowNum = 1
                      AND (rc.idrespuesta = 5 OR rc.feccomp IS NOT NULL OR al.autorizo = 'si');
                """

            # Ejecutamos la consulta
            cursor.execute(query)

            # Obtenemos las columnas y los datos
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

            # Convertimos los resultados a una lista de diccionarios
            result_list = [dict(zip(columns, row)) for row in data]

        except Exception as e:
            return Response({'error': str(e)}, status=500)

        finally:
            # Cerramos el cursor
            cursor.close()

        # Devolvemos la respuesta estructurada
        return Response(result_list)
    

#cantidad de Boletas pagada y en deuda
#pass
class BoletasPagadas(APIView):
    def get(self, request,  rut):
        cursor = connections['pass'].cursor()
        try:
            query = """
                    SELECT pd.customer_nid as Rut, pd.document_type,pd.document_issue_date,pd.document_expiration_date,pd.Mora,pd.saldo,
                    p.FECHA_PAGO, p.FOLIO 
                    FROM Cartera_Primer_Dia pd 
                    LEFT JOIN Cartera c ON c.document_legal_number = pd.document_legal_number
                    inner join Pagos p on pd.document_legal_number = p.FOLIO
                    WHERE pd.customer_nid = %s AND c.document_legal_number IS NULL
                """
            cursor.execute(query, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

            result_list = [dict(zip(columns, row)) for row in data]
            return Response(result_list, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            cursor.close()  # Cerrar el cursor correctamente

#pass
class BoletasPagadasSvia(APIView):
    def get(self, request, rut):
        cursor = connections['svia'].cursor()
        try:
            query = """
                SELECT pd.Rut, pd.Fec_Emi,pd.Fec_Vcto,pd.Monto_Pago, pd.Fecha_Pago,pd.Folio
                FROM cartera_primer_dia c
                INNER JOIN Pagos_Doc pd ON c.Folio = pd.Folio 
                WHERE c.RutDV = %s
            """
            cursor.execute(query, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

            result_list = [dict(zip(columns, row)) for row in data]
            return Response(result_list, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the exception if needed
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            cursor.close()  # Ensure the cursor is closed



#name of executive for register gestion
class getNameExecutiveForWallet(APIView): 
    def get(self, request, tipo):
        try:
            with connections['storage'].cursor() as cursor:
                # Usar un parámetro en lugar de un valor fijo
                cursor.execute("""
                    EXEC [getExecutiveWallet] %s
                """, [tipo])  # Usar %s como marcador de posición para el parámetro

                # Obtener nombres de las columnas
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

            # Si no hay resultados, devolver un mensaje informativo
            if not data:
                return Response({'message': 'No se encontraron datos disponibles'}, status=200)

            # Convertir los resultados a una lista de diccionarios
            result_list = [dict(zip(columns, row)) for row in data]
            return Response(result_list)
        
        except Exception as e:
            # Manejar errores en la ejecución
            return Response({'error': str(e)}, status=500)
      
     
        
        
class getPagosEjecutivosWallet(APIView):
    def get(self, request, ruteje,tipo):
        # Verificar si la conexión existe
        try:
            with connections[tipo].cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM [dbo].[fn_pagos_total]() WHERE ruteje = %s;
                """, [ruteje])  # Usar el parámetro ruteje de forma segura
                
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

            # Si no hay resultados en la consulta, devolver un mensaje con HTTP 200
            if not data:
                return Response({'message': 'No se encontraron datos disponibles'}, status=200)

            result_list = [dict(zip(columns, row)) for row in data]
            return Response(result_list)
        
        except Exception as e:
            # Manejar errores y devolver un mensaje con HTTP 500
            return Response({'error': str(e)}, status=500)


#move
class getRecuperoEjecutivos(APIView):
    """View for retrieving data from the fn_pagos_total stored function."""
    def get(self, request, tipo):
        """Handle GET requests to retrieve payment totals."""
        try:
            with connections[tipo].cursor() as cursor:
                cursor.execute("SELECT * FROM [dbo].[fn_pagos_total]();")
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

            if not data:
                return Response({'message': 'No se encontraron datos disponibles'}, status=200)

            result_list = [dict(zip(columns, row)) for row in data]
            return Response(result_list)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
class getCuotasAvo(APIView):
    def get(self, request, rut):
        try:
            query = """
                SELECT  c.RutDV, sum(c.consumoMes) AS ConsumoMes, sum(c.CuotaMes) AS CuotaMes, (sum(c.consumoMes) + sum(c.CuotaMes)) AS Total, 
                max(c.EstadoRepactacion) AS EstadoRepactacion, max(c.CuotasFuturas) AS CuotasFuturas
                FROM Cartera c WHERE rutdv = %s GROUP BY c.RutDV
            """
            with connections['avo'].cursor() as cursor:
                cursor.execute(query, [rut])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            if not rows:
                return Response({'message': 'No se encontraron datos disponibles'}, status=200)

            result_list = [dict(zip(columns, row)) for row in rows]
            return Response(result_list, status=200)

        except Exception as e:
            return Response({'error': 'Error interno: ' + str(e)}, status=500)