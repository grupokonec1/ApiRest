from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from datetime import datetime,timedelta,timezone
from rest_framework import generics
from django.http import JsonResponse
from django.db import connections, transaction
from rest_framework.views import APIView
from rest_framework import status
import requests
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import paramiko
from django.http import JsonResponse, FileResponse, HttpResponse
import os
import json
from rest_framework.parsers import MultiPartParser
from stat import S_ISDIR
import urllib.parse
from django.core.files.storage import default_storage
from django.core.cache import cache
from django.views import View
from django.utils.decorators import method_decorator
from smb.SMBConnection import SMBConnection
import tempfile
import jwt
from rest_framework.exceptions import AuthenticationFailed
from io import BytesIO
from Api.models import UserLogin
from Api.k3.helpers.jwt import generate_jwt_token, verify_jwt, generate_jwt_token_non_expiring, generate_jwt_token_expiring

@api_view(['GET'])
def generar_reporte_externo(request):
    fecha_inicio = request.query_params.get('fecha_inicio') 
    fecha_fin = request.query_params.get('fecha_fin')
    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y').date() 
        fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y').date()
    except ValueError:
        return Response({'error': 'Formato de fecha incorrecto. Use formato DD-MM-YYYY.'}, status=400)
    try:
        with connections['svia'].cursor() as cursor:
            query = "EXEC proc_reporte_gestiones_fechas @inicio = %s, @fin = %s"
            cursor.execute(query, [fecha_inicio, fecha_fin]) 
            result = cursor.fetchall()
        result_list = [list(row) for row in result]
        return Response(result_list)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def generar_reporte_interno(request):
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y').date()
        fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y').date()
    except ValueError as e:
        return Response({'error': 'Formato de fecha incorrecto. Use formato DD-MM-YYYY.'}, status=400)
    
    try:
        with connections['svia'].cursor() as cursor:
            query = "EXEC proc_gestion_ayer_fec @FechaInicio = %s, @FechaFin = %s"
            cursor.execute(query, [fecha_inicio, fecha_fin])  # Pasar las fechas como parámetros
            
            result = cursor.fetchall()
        
        result_list = [list(row) for row in result]
        return Response(result_list)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

#vista 

class InformeGestionToday(APIView):
    def get(self, request):
        cursor = connections['svia'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM vw_informe_gestion_diaria
            """)
            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Asegurarse de cerrar el cursor correctamente

        # Convertir los resultados a una lista de diccionarios (clave: nombre de columna)
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)


class RecordingSviaView(APIView):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        cursor = connections['vici'].cursor()
        try:
            cursor.execute("""
                
SELECT 
    t.Nombre AS status,
    l.address2 AS Rut,
    nu.nombre AS Nombre_Eje,
    l.vt_comments,
    l.location,
    l.call_date
FROM 
    VICI.dbo.Logs l
INNER JOIN
    report00.dbo.SAC_Svia_Tipificaciones t
ON 
    l.status = t.Abreviatura
INNER JOIN 
    report00.dbo.new_usuers nu
ON 
    nu.rut = l.[user]
WHERE 
    l.campaign_id = 'SOCIEDADCONCESIONARI' 
AND CONVERT(DATE,l.call_date)  >= %s
AND CONVERT(DATE,l.call_date) <= %s
                           
            """, [start_date, end_date])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()

        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
    




@api_view(['GET'])
def get_audio_files(request):
    hostname = '192.168.5.18'
    port = 22
    username = 'Administrador'
    password = 'Kon3ctados2024;'
    remote_directory = 'C:\\GRABACIONES'

    name = request.GET.get('name')
    
    if not name:
        return JsonResponse({'error': 'El parámetro name es requerido.'}, status=400)
    
    matching_files = []
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname, port, username, password)
        sftp_client = ssh_client.open_sftp()
        files = sftp_client.listdir(remote_directory)
        for file in files:
            if file.endswith(".mp3") and name in file:
                matching_files.append(file)

        sftp_client.close()
        ssh_client.close()

        return JsonResponse({'files': matching_files})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)






@api_view(['GET'])
def download_file(request, file_name):
    hostname = '192.168.5.18'
    port = 22
    username = 'Administrador'
    password = 'Kon3ctados2024;'
    remote_directory = 'C:\\GRABACIONES'


    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname, port, username, password)
        sftp_client = ssh_client.open_sftp()

        remote_file_path = os.path.join(remote_directory, file_name)
        
       
        with sftp_client.file(remote_file_path, 'rb') as remote_file:
            file_content = remote_file.read()

       
        sftp_client.close()
        ssh_client.close()

        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




#---------------------------------------------------------------------
#for delete 
@csrf_exempt
def proxy_view(request):
    if request.method == 'GET':
        params = request.GET
        url = 'https://konectados.integradial.us/agc/api.php'

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Levanta un error para códigos de estado HTTP 4xx/5xx
            return JsonResponse(response.json())
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=response.status_code if response else 500)
        except ValueError as ve:
            return JsonResponse({'error': 'Error en la respuesta JSON: {}'.format(ve)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


#gmini
@csrf_exempt
def proxyGmini_view(request):
    if request.method == 'POST':
        try:
            url = 'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key=AIzaSyCQj2I6MA1a1--v0QagV0oFXI5jEcndc1g'

            payload = json.loads(request.body)

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            respuesta_texto = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return JsonResponse({"text": respuesta_texto})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def nonAgentApi(request):
    if request.method == 'GET':
        params = request.GET
        url = 'https://konectados.integradial.us/vicidial/non_agent_api.php'

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Levanta un error para códigos de estado HTTP 4xx/5xx
            
            # Devuelve el contenido tal como viene
            return JsonResponse({'data': response.text}, safe=False)
        
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=response.status_code if response else 500)
        
    return JsonResponse({'error': 'Método no permitido'}, status=405)

class DeadCallInsertView(APIView):
    def get(self, request):
        # Extraer los parámetros enviados por Vicidial
        lead_id = request.GET.get('lead_id')
        user = request.GET.get('user')
        phone_number = request.GET.get('phone')

        # Validar solo los parámetros disponibles
        if not all([lead_id, user, phone_number]):
            return JsonResponse({'error': 'Faltan parámetros en la solicitud'}, status=400)

        try:
            # Insertar los datos en la base de datos
            with connections['api'].cursor() as cursor:
                query = """
                    INSERT INTO Prueba (lead_id, [user], phone_number)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, [lead_id, user, phone_number])
            return JsonResponse({'message': 'Datos insertados correctamente'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



#audios 
class RecordingAllWalletView(APIView):
    def get(self, request):
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        source = request.GET.get('tipo')  # Este es el parámetro que puede contener múltiples valores
        wallet = request.GET.get('wallet')

        if not start_date_str or not end_date_str or not source or not wallet:
            return Response({'error': 'Missing required parameters. Please provide start_date, end_date, source, and wallet.'}, status=400)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        search_terms = source.split()

        if wallet.upper() == 'ACSA':
            db_name = 'ACSA'
            campaign1 = f"%{search_terms[0]}%" if len(search_terms) > 0 else '%'
            campaign2 = f"%{search_terms[1]}%" if len(search_terms) > 1 else '%'
            campaign3 = f"%{search_terms[2]}%" if len(search_terms) > 2 else '%'
            query = f"""
                SELECT DISTINCT
                    l.[user] AS Rut,
                    l.status,
                    l.location,
                    l.call_date,
                    l.vendor_lead_code,
                    rc.rut,
                    l.type,
                    l.campaign_id,
                    l.phone_number,
                    nu.nombre,
                    t.Tipo,
                    t.GLOSA_ESTADO,
                    rc.feccomp,
                    rc.glosa
                FROM
                    VICI.dbo.Logs l
                    INNER JOIN {db_name}.dbo.Registro_Contacto rc ON CAST(l.phone_number AS NVARCHAR) = rc.telefono
                    INNER JOIN report00.dbo.new_usuers nu ON l.[user] = nu.rut
                    INNER JOIN report00.dbo.Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
                WHERE
                    (l.campaign_id LIKE %s OR l.campaign_id LIKE %s OR l.campaign_id LIKE %s)
                    AND l.location IS NOT NULL
                    AND l.status NOT IN ('BZN', 'NC', 'FNC')
                    AND CONVERT(DATE, l.call_date) >= %s
                    AND CONVERT(DATE, l.call_date) <= %s
                    AND CONVERT(DATE, l.call_date) = CONVERT(DATE, rc.fecha)
                    AND t.status = l.status
            """
            params = [campaign1, campaign2, campaign3, start_date, end_date]
        else:
            db_name = wallet.upper()
            campaign = f"%{search_terms[0]}%" if search_terms else '%' # Manejo si no hay términos de búsqueda
            query = """
                SELECT DISTINCT
                    l.[user] AS Rut,
                    l.status,
                    l.location,
                    l.call_date,
                    l.vendor_lead_code,
                    rc.rut,
                    l.type,
                    l.campaign_id,
                    l.phone_number,
                    nu.nombre,
                    t.Tipo,
                    t.GLOSA_ESTADO,
                    rc.feccomp,
                    rc.glosa
                FROM
                    VICI.dbo.Logs l
                    INNER JOIN {}.dbo.Registro_Contacto rc ON CAST(l.phone_number AS NVARCHAR) = rc.telefono
                    INNER JOIN report00.dbo.new_usuers nu ON l.[user] = nu.rut
                    INNER JOIN report00.dbo.Tipificaciones t ON rc.idrespuesta = t.Idrespuesta
                WHERE
                    l.campaign_id LIKE %s
                    AND l.location IS NOT NULL
                    AND l.status NOT IN ('BZN', 'NC', 'FNC')
                    AND CONVERT(DATE, l.call_date) >= %s
                    AND CONVERT(DATE, l.call_date) <= %s
                    AND CONVERT(DATE, l.call_date) = CONVERT(DATE, rc.fecha)
                    AND t.status = l.status
                    AND l.[user] = rc.ruteje
            """.format(db_name)
            params = [campaign, start_date, end_date]

        cursor = connections['vici'].cursor()
        try:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        except Exception as e:
            cursor.close()
            return Response({'error': f'Database error: {e}'}, status=500)
        finally:
            cursor.close()

        result_list = [dict(zip(columns, row)) for row in data]

        # Reemplazar IPs por URLs en la columna "location"
        ip_to_url = {
            "82.197.64.168": "konectadosvc1.integradial.us",
            "82.197.64.169": "konectadosvc2.integradial.us",
            "154.38.181.115": "konectadosvc3.integradial.us",
            "154.38.181.116": "konectadosvc4.integradial.us",
            "200.39.137.83": "konectadosast1.integradial.us",
            "200.39.137.84": "konectadosast2.integradial.us"
        }

        for record in result_list:
            for ip, url in ip_to_url.items():
                if ip in record['location']:
                    record['location'] = record['location'].replace(ip, url)

        return Response(result_list, status=200)


  

def convert_date(date_str):
    """Convierte una cadena de fecha en formato aceptable por SQL Server, o retorna None si no es válida."""
    if date_str in (None, '', '0000-00-00'):
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def get_value(item, key, expected_type=None):
    """Retorna el valor asociado a una clave o None si la clave no existe en el diccionario.
    Opcionalmente convierte el valor al tipo esperado."""
    value = item.get(key, None)
    if value is None or value == '':
        return None
    if expected_type and value is not None:
        try:
            if expected_type == int:
                return int(value)
            elif expected_type == float:
                return float(value)
            elif expected_type == str:
                return str(value)
        except (ValueError, TypeError):
            return None
    return value

@csrf_exempt
def insert_logs(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            list_id = data.get('list_id')
            
            if not list_id or not isinstance(list_id, int):
                return JsonResponse({'error': 'Invalid or missing list_id'}, status=400)
            
            api_url = "https://konectados.integradial.us/vicidial/customs/get_calls.php"
            uno = datetime.now()
            today = uno.strftime('%Y-%m-%d')
            payload = {"startDate": today, "endDate": today, "list_id": list_id}
            
            # Realiza la solicitud HTTP GET al endpoint con el cuerpo JSON
            response = requests.get(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            
            if response.status_code == 200:
                try:
                    external_data = response.json()
                except ValueError:
                    return JsonResponse({'error': 'Error parsing JSON from external API'}, status=500)
                
                # Verificar el contenido de la respuesta
                if not isinstance(external_data, list):
                    return JsonResponse({'error': 'Expected a list from external API', 'response': external_data}, status=500)
                
                columns = [
                    'uniqueid', 'lead_id', 'list_id', 'campaign_id', 'call_date', 'length_in_sec', 'status', 'phone_code', 'phone_number',
                    '[user]', 'comments', 'processed', 'user_group', 'term_reason', 'called_count', 'entry_date', 'modify_date', 'vendor_lead_code',
                    'source_id', 'gmt_offset_now', 'called_since_last_reset', 'title', 'first_name', 'middle_initial', 'last_name', 'address1',
                    'address2', 'address3', 'city', 'state', 'province', 'postal_code', 'country_code', 'gender', 'date_of_birth', 'alt_phone',
                    'email', 'security_phrase', 'last_local_call_time', 'rank', 'owner', 'entry_list_id', 'type', 'filename', 'location','vt_phone_code',
                    'vt_phone_number','vt_comments','vt_called_count'
                ]

                existing_data_count = 0
                new_data_count = 0

                # Conecta a la base de datos y verifica si ya existen antes de insertar
                with connection.cursor() as cursor:
                    for record in external_data:
                        uniqueid = record.get('uniqueid')
                        if uniqueid is None:
                            continue
                        
                        cursor.execute("SELECT COUNT(*) FROM VICI.dbo.Logs WHERE uniqueid = %s", [uniqueid])
                        count = cursor.fetchone()[0]
                        
                        if count == 0:
                            values = [
                                get_value(record, 'uniqueid', str), get_value(record, 'lead_id', int), get_value(record, 'list_id', int), get_value(record, 'campaign_id', str),
                                convert_date(get_value(record, 'call_date', str)), get_value(record, 'length_in_sec', int), get_value(record, 'status', str),
                                get_value(record, 'phone_code', int), get_value(record, 'phone_number', int), get_value(record, 'user', str), get_value(record, 'comments', str),
                                get_value(record, 'processed', str), get_value(record, 'user_group', str), get_value(record, 'term_reason', str), get_value(record, 'called_count', int),
                                convert_date(get_value(record, 'entry_date', str)), convert_date(get_value(record, 'modify_date', str)), get_value(record, 'vendor_lead_code', str),
                                get_value(record, 'source_id', str), get_value(record, 'gmt_offset_now', float), get_value(record, 'called_since_last_reset', str), get_value(record, 'title', str),
                                get_value(record, 'first_name', str), get_value(record, 'middle_initial', str), get_value(record, 'last_name', str), get_value(record, 'address1', str),
                                get_value(record, 'address2', str), get_value(record, 'address3', str), get_value(record, 'city', str), get_value(record, 'state', str), get_value(record, 'province', str),
                                get_value(record, 'postal_code', str), get_value(record, 'country_code', str), get_value(record, 'gender', str), convert_date(get_value(record, 'date_of_birth', str)),
                                get_value(record, 'alt_phone', int), get_value(record, 'email', str), get_value(record, 'security_phrase', str), convert_date(get_value(record, 'last_local_call_time', str)),
                                get_value(record, 'rank', int), get_value(record, 'owner', str), get_value(record, 'entry_list_id', int), get_value(record, 'type', str), get_value(record, 'filename', str),
                                get_value(record, 'location', str), get_value(record, 'vt_phone_code', str),get_value(record, 'vt_phone_number', str),get_value(record, 'vt_comments', str), get_value(record, 'vt_called_count', str)
                            ]

                            cursor.execute(f"""
                                INSERT INTO VICI.dbo.Logs ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})
                            """, values)
                            new_data_count += 1
                        else:
                            existing_data_count += 1

                if new_data_count > 0:
                    return JsonResponse({'message': 'Data inserted successfully'}, status=200)
                else:
                    return JsonResponse({'message': 'All data already exists'}, status=200)
            
            return JsonResponse({'error': 'Failed to fetch data from external API'}, status=500)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


class ListNASFilesView(APIView):
    def get(self, request):
        server = "192.168.5.10"
        share = "respaldo_KON3CTADOS"
        username = "kon3ctados"
        password = "icxnas2024"
        client_machine_name = "my_client"
        server_name = "my_server"
        directory_path = "Documentos/Mirror"

        try:
            # Conectar al servidor NAS
            conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)
            assert conn.connect(server, 139)

            # Función para listar archivos y carpetas de forma recursiva
            def list_files_recursive(conn, share, path):
                files = []
                for file in conn.listPath(share, path):
                    if file.filename not in ['.', '..']:
                        file_path = f"{path}/{file.filename}"
                        if file.isDirectory:
                            files.append({
                                "name": file.filename,
                                "path": file_path,
                                "type": "directory",
                                "children": list_files_recursive(conn, share, file_path)
                            })
                        else:
                            files.append({
                                "name": file.filename,
                                "path": file_path,
                                "type": "file"
                            })
                return files

            # Obtener la lista de archivos y carpetas
            file_list = list_files_recursive(conn, share, directory_path)

            # Cerrar la conexión SMB
            conn.close()

            return Response({"files": file_list}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class ListNASFilesRRHHView(APIView):
    def get(self, request):
        server = "192.168.5.10"
        share = "respaldo_KON3CTADOS"
        username = "kon3ctados"
        password = "icxnas2024"
        client_machine_name = "my_client"
        server_name = "my_server"
        directory_path = "RR_HH"

        try:
            # Conectar al servidor NAS
            conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)
            assert conn.connect(server, 139)

            # Función para listar archivos y carpetas de forma recursiva
            def list_files_recursive(conn, share, path):
                files = []
                for file in conn.listPath(share, path):
                    if file.filename not in ['.', '..']:
                        file_path = f"{path}/{file.filename}"
                        if file.isDirectory:
                            files.append({
                                "name": file.filename,
                                "path": file_path,
                                "type": "directory",
                                "children": list_files_recursive(conn, share, file_path)
                            })
                        else:
                            files.append({
                                "name": file.filename,
                                "path": file_path,
                                "type": "file"
                            })
                return files

            # Obtener la lista de archivos y carpetas
            file_list = list_files_recursive(conn, share, directory_path)

            # Cerrar la conexión SMB
            conn.close()

            return Response({"files": file_list}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        
class DownloadNASFileView(APIView):
    def get(self, request):
        file_path = request.GET.get('file_path')
        if not file_path:
            return Response({"error": "file_path is required"}, status=400)

        server = "192.168.5.10"
        share = "respaldo_KON3CTADOS"
        username = "kon3ctados"
        password = "icxnas2024"
        client_machine_name = "my_client"
        server_name = "my_server"

        try:
            # Construir la ruta completa del archivo (sin agregar el directory_path)
            full_file_path = f"{urllib.parse.unquote(file_path)}"

            # Depuración: imprimir la ruta completa
            print(f"Ruta completa construida: {full_file_path}")

            # Conectar al servidor NAS
            conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)
            if not conn.connect(server, 139):
                return Response({"error": "Could not connect to the server."}, status=500)

            # Crear un objeto BytesIO para almacenar el archivo descargado
            file_obj = BytesIO()

            # Descargar el archivo desde el NAS
            conn.retrieveFile(share, full_file_path, file_obj)

            # Cerrar la conexión SMB
            conn.close()

            # Preparar el archivo para la respuesta HTTP
            file_obj.seek(0)
            response = HttpResponse(file_obj, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'

            return response

        except Exception as e:
            # Manejo de errores más detallado para identificar la causa del problema
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)



class PreviewNASFileView(APIView):
    def get(self, request):
        file_path = request.GET.get('file_path')
        if not file_path:
            return Response({"error": "file_path is required"}, status=400)

        server = "192.168.5.10"
        share = "respaldo_KON3CTADOS"
        username = "kon3ctados"
        password = "icxnas2024"
        client_machine_name = "my_client"
        server_name = "my_server"

        try:
            # Construir la ruta completa del archivo
            full_file_path = f"{urllib.parse.unquote(file_path)}"

            # Conectar al servidor NAS
            conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)
            if not conn.connect(server, 139):
                return Response({"error": "Could not connect to the server."}, status=500)

            # Crear un objeto BytesIO para almacenar el archivo descargado
            file_obj = BytesIO()

            # Descargar el archivo desde el NAS
            conn.retrieveFile(share, full_file_path, file_obj)

            # Cerrar la conexión SMB
            conn.close()

            # Determinar el tipo de contenido en función de la extensión del archivo
            file_extension = full_file_path.split('.')[-1].lower()
            if file_extension == 'pdf':
                content_type = 'application/pdf'
            elif file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                content_type = f'image/{file_extension}'
            elif file_extension in ['doc', 'docx']:
                content_type = 'application/msword'
            elif file_extension == 'xlsx':
                content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            else:
                content_type = 'application/octet-stream'

            # Preparar el archivo para la respuesta HTTP
            file_obj.seek(0)
            response = HttpResponse(file_obj, content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{file_path.split("/")[-1]}"'

            return response

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)
        
        
        
#cambiar que apunte al nas
class UploadSFTPFileView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        host = "192.168.5.13"
        port = 22
        username = "libreria"
        password = "n7ylwjsps3"

        transport = None
        sftp = None

        try:
            path = request.data.get('path', '').strip('/')
            file = request.FILES.get('file')

            if not path or not file:
                return JsonResponse({"error": "El path y el archivo son requeridos"}, status=400)

            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Asegurarse de que el archivo se guarda en la ruta correcta
            full_path = os.path.join(path, file.name).replace('\\', '/')
            with sftp.open(full_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # Limpiar el caché para la ruta actual
            cache_key = f"sftp_files_{path}"
            cache.delete(cache_key)

            return JsonResponse({"message": "Archivo subido con éxito"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            if sftp is not None:
                sftp.close()
            if transport is not None:
                transport.close()

#cambiar que apunte al Nas
class CreateSFTPDirectoryView(APIView):
    def post(self, request):
        host = "192.168.5.13"
        port = 22
        username = "libreria"
        password = "n7ylwjsps3"

        transport = None
        sftp = None

        try:
            data = request.data
            directory_path = data.get('path', '').strip('/')
            directory_name = data.get('name', '').strip()

            if not directory_path or not directory_name:
                return JsonResponse({"error": "El path y el nombre son requeridos"}, status=400)

            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Asegurarse de que el nuevo directorio se crea dentro de la carpeta seleccionada
            full_path = os.path.join(directory_path, directory_name).replace('\\', '/')
            sftp.mkdir(full_path)

            # Limpiar el caché para la ruta actual
            cache_key = f"sftp_files_{directory_path}"
            cache.delete(cache_key)

            return JsonResponse({"message": "Directorio creado con éxito"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            if sftp is not None:
                sftp.close()
            if transport is not None:
                transport.close()

class ListSMBFilesUniqueView(APIView):
    def post(self, request):
        server = "192.168.5.10"
        share = "respaldo_KON3CTADOS"
        username = "kon3ctados"
        password = "icxnas2024"
        client_machine_name = "my_client"
        server_name = "my_server"

        try:
            directory_name = request.data.get('directory_name', '')
            if not directory_name:
                return JsonResponse({"error": "No directory name provided"}, status=400)

            base_path = "Documentos/Mirror"
            target_path = f"{base_path}/{directory_name}"

            conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)
            assert conn.connect(server, 139)

            def list_files_recursive(conn, share, path):
                files = []
                try:
                    for entry in conn.listPath(share, path):
                        if entry.filename not in ['.', '..']:
                            entry_path = f"{path}/{entry.filename}"
                            if entry.isDirectory:
                                files.append({
                                    "name": entry.filename,
                                    "path": entry_path,
                                    "type": "directory",
                                    "children": list_files_recursive(conn, share, entry_path)
                                })
                            else:
                                files.append({
                                    "name": entry.filename,
                                    "path": entry_path,
                                    "type": "file"
                                })
                except Exception as e:
                    return {"error": str(e)}
                return files

            directory_name = urllib.parse.unquote(directory_name)
            files_list = list_files_recursive(conn, share, target_path)

            conn.close()

            return JsonResponse({"files": files_list}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class ListSMBFilesRrrHhView(APIView):
    def post(self, request):
        server = "192.168.5.10"
        share = "respaldo_KON3CTADOS"
        username = "kon3ctados"
        password = "icxnas2024"
        client_machine_name = "my_client"
        server_name = "my_server"

        try:
            directory_name = request.data.get('directory_name', '')
            if not directory_name:
                return JsonResponse({"error": "No directory name provided"}, status=400)

            base_path = "RR_HH"
            target_path = f"{base_path}/{directory_name}"

            conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)
            assert conn.connect(server, 139)

            def list_files_recursive(conn, share, path):
                files = []
                try:
                    for entry in conn.listPath(share, path):
                        if entry.filename not in ['.', '..']:
                            entry_path = f"{path}/{entry.filename}"
                            if entry.isDirectory:
                                files.append({
                                    "name": entry.filename,
                                    "path": entry_path,
                                    "type": "directory",
                                    "children": list_files_recursive(conn, share, entry_path)
                                })
                            else:
                                files.append({
                                    "name": entry.filename,
                                    "path": entry_path,
                                    "type": "file"
                                })
                except Exception as e:
                    return {"error": str(e)}
                return files

            directory_name = urllib.parse.unquote(directory_name)
            files_list = list_files_recursive(conn, share, target_path)

            conn.close()

            return JsonResponse({"files": files_list}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



class InsertFileSFTPView(APIView):
    def post(self, request):
        host = "192.168.5.12"
        port = 21
        username = "UsrK3"
        password = "KqoVd3AdwrYwWfP"
        remote_path = "L:\\DOCUMENTOS\\Produccion\\Push\\CONDEZA\\"
        
        if 'file' not in request.FILES:
            return Response({'error': 'No se proporcionó el archivo.'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        local_path = default_storage.save(file.name, file)

        try:
          
            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
        
            if not remote_path.endswith("\\"):
                remote_path += "\\"
            
          
            sftp.put(local_path, remote_path + file.name)
         
            sftp.close()
            transport.close()
            
         
            if os.path.exists(local_path):
                os.remove(local_path)
            
            return Response({'message': 'Archivo subido exitosamente.'}, status=status.HTTP_200_OK)
        except Exception as e:
            
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           

class CleanFolderSFTPView(APIView):
    def post(self, request):
        host = "192.168.5.11"
        port = 22
        username = "administrador"
        password = "Kon3ctados2024-"
        remote_path = "C:\\Users\\Administrador\\Documents\\Cargas\\CONDEZA\\"

        try:
            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Listar y eliminar todos los archivos en el directorio
            for filename in sftp.listdir(remote_path):
                filepath = remote_path + filename
                sftp.remove(filepath)

            sftp.close()
            transport.close()

            return Response({'message': 'Carpeta limpia exitosamente.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListFilesServerView(APIView):
    def get(self, request):
        host = "192.168.5.11"
        port = 22
        username = "administrador"
        password = "Kon3ctados2024+"
        remote_path = "C:\\Users\\Administrador\\Documents\\Cargas\\CONDEZA\\"

        try:
            # Conectar al servidor de la base de datos mediante SSH
            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Listar los archivos en el directorio remoto
            files = sftp.listdir(remote_path)

            sftp.close()
            transport.close()

            return Response({'files': files}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#users
@method_decorator(csrf_exempt, name='dispatch')
class getUsersAsigned(View):
    def post(self, request):
        import json
        try:
            data = json.loads(request.body)
            rutdv = data.get('rutdv', None)
            if rutdv is None:
                return JsonResponse({'error': 'Parameter "rutdv" is required'}, status=400)
            
            with connection.cursor() as cursor:
                query = """
                    SELECT [file] 
                    FROM konexnet.dbo.Asignacion 
                    WHERE Usuarios_idUsuarios = %s 
                      AND [file] IS NOT NULL
                """
                cursor.execute(query, [rutdv])
                result = cursor.fetchall()
                
            files = [row[0] for row in result]
            return JsonResponse({'files': files}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)        

class getAllUsers(APIView):
    def get(self, request):
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                SELECT idUser,NameUser,Rut, Correo, a.NameAreas, r.NameRol  FROM Users
                INNER JOIN Areas a ON Users.idArea = a.idAreas
                INNER JOIN Roles r ON Users.idRol = r.idRol
            """)
            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Asegurarse de cerrar el cursor correctamente

        # Convertir los resultados a una lista de diccionarios (clave: nombre de columna)
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)

class getLoginUser(APIView):
    def get(self, request):
        rut = request.GET.get('rut')
        password = request.GET.get('password')

        if not rut or not password:
            return Response({'ok': False, 'error': 'El "rut" o "password" incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

        cursor = connections['api'].cursor()
        try:
            # Obtener usuario con su token
            cursor.execute(
                "SELECT idUser, NameUser, Correo, idRol, Rut, token FROM Users WHERE Rut = %s", [rut]
            )
            data = cursor.fetchone()
        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()

        if not data:
            return Response({'ok': False, 'error': 'Usuario no encontrado'}, status=status.HTTP_401_UNAUTHORIZED)

        id_user = data[0]
        user_data = {
            "NameUser": data[1],
            "Correo": data[2],
            "idRol": data[3],
            "Rut": data[4]
        }
        current_token = data[5]

        if current_token:
            # Verificar si el token es válido
            try:
                verify_jwt(current_token)  # Si no lanza excepción, el token sigue siendo válido
                return Response({'ok': True, 'token': current_token, 'user': user_data}, status=status.HTTP_200_OK)
            except AuthenticationFailed as e:
                if str(e) == 'El token ha expirado':
                    # Generar un nuevo token si expiró
                    new_token = generate_jwt_token(id_user, user_data["Rut"])
                    
                    # Actualizar el token en la base de datos
                    update_cursor = connections['api'].cursor()
                    try:
                        update_cursor.execute("UPDATE Users SET token = %s WHERE idUser = %s", [new_token, id_user])
                    except Exception as e:
                        return Response({'ok': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    finally:
                        update_cursor.close()
                    
                    return Response({'ok': True, 'token': new_token, 'user': user_data}, status=status.HTTP_200_OK)
                else:
                    return Response({'ok': False, 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'ok': False, 'error': 'Usuario no tiene un token asignado'}, status=status.HTTP_401_UNAUTHORIZED)


class getModulesUser(APIView):   
    def get(self, request):
        # Obtener el token del encabezado de autorización
        token = request.GET.get('x-token')

        if not token:
            return Response({'ok': False, 'error': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Verificar y decodificar el token
            decoded_token = verify_jwt(token)
            rut_from_token = decoded_token.get('rut')
        except AuthenticationFailed as e:
            return Response({'ok': False, 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Verificar si el RUT está en el token decodificado
        if not rut_from_token:
            return Response({'ok': False, 'error': 'RUT no encontrado en el token'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el token coincide en la base de datos y obtener el nombre del usuario
        cursor = connections['api'].cursor()
        try:
            cursor.execute("SELECT NameUser, token FROM Users WHERE Rut = %s", [rut_from_token])
            user_data = cursor.fetchone()

            if not user_data or user_data[1] != token:
                return Response({'ok': False, 'error': 'Token inválido o no coincide'}, status=status.HTTP_401_UNAUTHORIZED)
            
            user_name = user_data[0]  # Obtener el nombre del usuario desde la consulta

            # Si el token es válido, realizar la consulta utilizando el RUT para obtener los módulos y carteras
            cursor.execute("""
                SELECT
                  w.idWallet,
                  w.NameWallet
                FROM Users u1
                INNER JOIN PermissionsWallet pw ON u1.idUser = pw.idUser 
                INNER JOIN Wallet w ON pw.idWallet = w.idWallet
                WHERE u1.Rut = %s AND pw.active = 1
                
                UNION
                
                SELECT
                  m.idModule,
                  m.NameModule
                FROM Users u2
                INNER JOIN PermissionsModule pm ON u2.idUser = pm.idUser
                INNER JOIN Module m ON pm.idModule = m.idModule
                WHERE u2.Rut = %s AND pm.active = 1
            """, [rut_from_token, rut_from_token])  # Usar el RUT del token para la consulta

            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()
        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        finally:
            cursor.close()
        
        # Verificar si se encontró información
        if data:
            result_list = [dict(zip(columns, row)) for row in data]
            return Response({'ok': True, 'user': user_name, 'data': result_list}, status=status.HTTP_200_OK)
        else:
            return Response({'ok': False, 'user': user_name, 'data': []}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):   
    def post(self, request):
        data = request.data
        try:
            # Verificar si el RUT ya existe en la base de datos
            if UserLogin.objects.filter(Rut=data.get('Rut')).exists():
                return Response({'error': 'Usuario ya existe en la base'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear el usuario y guardarlo en la base de datos con la fecha y hora de creación
            user = UserLogin.objects.create(
                NameUser=data.get('NameUser'),
                Correo=data.get('Correo'),
                Password=data.get('Password'),  # Asegúrate de cifrar la contraseña antes de guardar
                idArea=data.get('idArea'),
                idRol=data.get('idRol'),
                Rut=data.get('Rut'),
                dateCreation=datetime.now()  # Guarda fecha y hora completa
            )

            # Generar el token JWT utilizando la función separada
            token = generate_jwt_token(user.idUser, user.Rut)

            # Guardar el token en la base de datos
            user.token = token
            user.save()

            # Conectar con la base de datos `api`
            with connections['api'].cursor() as cursor:
                try:
                    cursor.execute("SELECT NameRol FROM Roles WHERE idRol = %s", [user.idRol])
                    role_data = cursor.fetchone()

                    if role_data and role_data[0] == 'Administrador':
                        cursor.execute("SELECT idModule FROM Module WHERE NameModule = 'Asignacion'")
                        module_data = cursor.fetchone()

                        if module_data:
                            id_module = module_data[0]
                            
                            # Insertar en la tabla PermissionsModule
                            cursor.execute(
                                "INSERT INTO PermissionsModule (idModule, idUser, active) VALUES (%s, %s, %s)",
                                [id_module, user.idUser, 1]
                            )
                            connections['api'].commit()  # Asegurar cambios en algunas configuraciones

                except Exception as e:
                    return Response({'error': f"Error al verificar o insertar permisos en 'api': {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Conectar con la base de datos `report`
            with connections['report'].cursor() as cursor:
                try:
                    # Insertar en la tabla `new_users`
                    cursor.execute(
                        "INSERT INTO new_usuers (rut, nombre) VALUES (%s, %s)",
                        [user.Rut, user.NameUser]
                    )
                    connections['report'].commit()  # Asegurar cambios en algunas configuraciones

                except Exception as e:
                    return Response({'error': f"Error al insertar en 'new_users': {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'ok': True, 'message': 'Usuario creado exitosamente', 'token': token}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class getRoles(APIView):
    def get(self, request):
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM Roles
            """)
            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Asegurarse de cerrar el cursor correctamente

        # Convertir los resultados a una lista de diccionarios (clave: nombre de columna)
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
    
class getWallet(APIView):
    def get(self, request):
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM Wallet
            """)
            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Asegurarse de cerrar el cursor correctamente

        # Convertir los resultados a una lista de diccionarios (clave: nombre de columna)
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
    
class getModules(APIView):
    def get(self, request):
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM Module
            """)
            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Asegurarse de cerrar el cursor correctamente

        # Convertir los resultados a una lista de diccionarios (clave: nombre de columna)
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
    

class getAreas(APIView):
    def get(self, request):
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM Areas
            """)
            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Asegurarse de cerrar el cursor correctamente

        # Convertir los resultados a una lista de diccionarios (clave: nombre de columna)
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
    
    
    
    
class GetModulesUserForRut(APIView):    
    def get(self, request):
        # Obtener el RUT de la solicitud (parámetro de la URL)
        rut = request.GET.get('rut')

        if not rut:
            return Response({'ok': False, 'error': 'RUT no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        # Realizar la consulta utilizando el RUT proporcionado para obtener los módulos y carteras
        cursor = connections['api'].cursor()
        try:
            # Consulta para obtener los módulos y carteras asociados al usuario
            cursor.execute("""
                SELECT
                  w.idWallet,
                  w.NameWallet
                FROM Users u1
                INNER JOIN PermissionsWallet pw ON u1.idUser = pw.idUser 
                INNER JOIN Wallet w ON pw.idWallet = w.idWallet
                WHERE u1.Rut = %s AND pw.active = 1
                
                UNION
                
                SELECT
                  m.idModule,
                  m.NameModule
                FROM Users u2
                INNER JOIN PermissionsModule pm ON u2.idUser = pm.idUser
                INNER JOIN Module m ON pm.idModule = m.idModule
                WHERE u2.Rut = %s AND pm.active = 1
            """, [rut, rut])  # Usar el RUT proporcionado para la consulta

            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()
        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        finally:
            cursor.close()
        
        # Verificar si se encontró información
        if data:
            result_list = [dict(zip(columns, row)) for row in data]
            return Response({'ok': True, 'data': result_list}, status=status.HTTP_200_OK)
        else:
            return Response({'ok': False, 'data': []}, status=status.HTTP_200_OK)


class InsertOrUpdatePermissionsModuleView(APIView):
    def post(self, request):
        # Obtener los datos del cuerpo de la solicitud
        idModule = request.data.get('idModule')
        idUser = request.data.get('idUser')
        active = request.data.get('active')

        # Verificar que todos los campos fueron proporcionados
        if idModule is None or idUser is None or active is None:
            return Response({'ok': False, 'error': 'Todos los campos (idModule, idUser, active) son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        # Conectar a la base de datos
        cursor = connections['api'].cursor()  # Usar la conexión de la base de datos configurada
        try:
            # Verificar si el registro ya existe
            cursor.execute("""
                SELECT idPermissionsModule, active FROM PermissionsModule 
                WHERE idModule = %s AND idUser = %s
            """, [idModule, idUser])
            existing_record = cursor.fetchone()
            
            if existing_record:
                idPermissionsModule, current_active = existing_record

                # Si existe y el campo `active` es diferente al proporcionado, se actualiza
                if current_active != active:
                    cursor.execute("""
                        UPDATE PermissionsModule 
                        SET active = %s 
                        WHERE idPermissionsModule = %s
                    """, [active, idPermissionsModule])
                    
                    return Response({'ok': True, 'message': 'Registro actualizado correctamente'}, status=status.HTTP_200_OK)
                else:
                    return Response({'ok': False, 'message': 'El registro ya existe y está en el estado requerido'}, status=status.HTTP_200_OK)
            
            else:
                # Si no existe, realizar la inserción
                cursor.execute("""
                    INSERT INTO PermissionsModule (idModule, idUser, active)
                    VALUES (%s, %s, %s)
                """, [idModule, idUser, active])
                
                return Response({'ok': True, 'message': 'Registro insertado correctamente'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        finally:
            cursor.close()
            
            
class InsertOrUpdatePermissionsWalletView(APIView):
    def post(self, request):
        # Obtener los datos del cuerpo de la solicitud
        idWallet = request.data.get('idWallet')
        idUser = request.data.get('idUser')
        active = request.data.get('active')

        # Verificar que todos los campos fueron proporcionados
        if idWallet is None or idUser is None or active is None:
            return Response({'ok': False, 'error': 'Todos los campos (idWallet, idUser, active) son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        # Conectar a la base de datos
        cursor = connections['api'].cursor()  # Usar la conexión de la base de datos configurada
        try:
            # Verificar si el registro ya existe
            cursor.execute("""
                SELECT idPermissionsWallet, active FROM PermissionsWallet 
                WHERE idWallet = %s AND idUser = %s
            """, [idWallet, idUser])
            existing_record = cursor.fetchone()
            
            if existing_record:
                idPermissionsWallet, current_active = existing_record

                # Si existe y el campo `active` es diferente al proporcionado, se actualiza
                if current_active != active:
                    cursor.execute("""
                        UPDATE PermissionsWallet 
                        SET active = %s 
                        WHERE idPermissionsWallet = %s
                    """, [active, idPermissionsWallet])
                    
                    return Response({'ok': True, 'message': 'Registro actualizado correctamente'}, status=status.HTTP_200_OK)
                else:
                    return Response({'ok': False, 'message': 'El registro ya existe y está en el estado requerido'}, status=status.HTTP_200_OK)
            
            else:
                # Si no existe, realizar la inserción
                cursor.execute("""
                    INSERT INTO PermissionsWallet (idWallet, idUser, active)
                    VALUES (%s, %s, %s)
                """, [idWallet, idUser, active])
                
                return Response({'ok': True, 'message': 'Registro insertado correctamente'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        finally:
            cursor.close()
            
            
    
class getPermissionsModule(APIView):
    def get(self, request):
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM PermissionsModule
            """)
            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Asegurarse de cerrar el cursor correctamente

        # Convertir los resultados a una lista de diccionarios (clave: nombre de columna)
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
    
    
class getPermissionsWallet(APIView):
    def get(self, request):
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                SELECT * FROM PermissionsWallet
            """)
            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Asegurarse de cerrar el cursor correctamente

        # Convertir los resultados a una lista de diccionarios (clave: nombre de columna)
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)


class InsertModules(APIView):
    def post(self, request):
        name_module = request.data.get('nameModule')

        if not name_module:
            return Response({'error': 'El campo nameModule es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                INSERT INTO Module (NameModule) VALUES(%s)
            """, [name_module])
            connections['api'].commit()

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
        return Response({"ok":True,'message': 'Módulo insertado exitosamente'}, status=status.HTTP_201_CREATED)
    
    
    
class InsertWallets(APIView):
    def post(self, request):
        name_module = request.data.get('nameWallet')

        if not name_module:
            return Response({'error': 'El campo nameModule es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
        cursor = connections['api'].cursor()
        try:
            cursor.execute("""
                INSERT INTO Wallet (NameWallet) VALUES(%s)
            """, [name_module])
            connections['api'].commit()

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
        return Response({'ok':True,'message': 'Módulo insertado exitosamente'}, status=status.HTTP_201_CREATED)
    
    
#falta
class deleteUsersWalletModule(APIView): 
    def post(self, request):
        id_user = request.data.get('idUser')  # Obtiene el idUser del request
        
        if not id_user:
            return Response({'error': 'El campo idUser es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        cursor = connections['api'].cursor()
        try:
            # Elimina los módulos, carteras y finalmente el usuario basado en el idUser
            cursor.execute("""
               -- Eliminar módulos
               DELETE pm
               FROM PermissionsModule pm
               WHERE pm.idUser = %s;

               -- Eliminar carteras
               DELETE pw
               FROM PermissionsWallet pw
               WHERE pw.idUser = %s;

               -- Eliminar el usuario
               DELETE FROM Users
               WHERE idUser = %s;
            """, [id_user, id_user, id_user])  # Pasa id_user como parámetro tres veces para las tres eliminaciones

            # Confirmar la transacción
            connections['api'].commit()

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()

        return Response({'ok': True, 'message': 'El usuario y sus permisos fueron eliminados exitosamente'}, status=status.HTTP_200_OK)
    

class VerifyOrRefreshTokenView(APIView):

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'ok': False, 'error': 'Token no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verifica el token
            payload = verify_jwt(token)

            # Verifica si el token está por expirar (menos de 5 minutos)
            expiration_time = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
            time_left = expiration_time - datetime.now(timezone.utc)

            # Busca al usuario en la base de datos
            user = UserLogin.objects.filter(idUser=payload['idUser'], Rut=payload['rut']).first()
            if not user:
                return Response({'ok': False, 'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            # Verifica si el usuario tiene idRol == 1
            if user.idRol == 1:
                return Response({'ok': False, 'error': 'Permisos insuficientes'}, status=status.HTTP_403_FORBIDDEN)

            if time_left < timedelta(minutes=5):
                # Genera un nuevo token si está por expirar
                new_token = generate_jwt_token(payload['idUser'], payload['rut'])

                # Actualiza el token del usuario en la base de datos con SQL en la conexión 'api'
                with connections['api'].cursor() as update_cursor:
                    update_cursor.execute(
                        "UPDATE Users SET token = %s WHERE idUser = %s", 
                        [new_token, user.idUser]
                    )

                return Response({'ok': True, 'message': 'Token renovado', 'new_token': new_token}, status=status.HTTP_200_OK)

            # Si el token es válido y no está por expirar, solo devuelve un mensaje de éxito
            return Response({'ok': True, 'message': 'Token válido', 'user': user.NameUser}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            # Si el token ha expirado, genera uno nuevo
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
            new_token = generate_jwt_token(payload['idUser'], payload['rut'])

            # Actualiza el token del usuario en la base de datos con SQL en la conexión 'api'
            with connections['api'].cursor() as update_cursor:
                update_cursor.execute(
                    "UPDATE Users SET token = %s WHERE idUser = %s", 
                    [new_token, payload['idUser']]
                )
            
            return Response({'ok': True, 'message': 'Token expirado, se generó uno nuevo', 'new_token': new_token}, status=status.HTTP_200_OK)

        except jwt.InvalidTokenError:
            return Response({'ok': False, 'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
class ContactosDc(APIView): 
    def get(self, request):
        tipoDb = request.query_params.get('tipoDb')  # Obtiene el tipo de base de datos desde los parámetros de consulta

        if not tipoDb:
            return Response({'error': 'El parámetro tipoDb es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
        
        cursor = connections[tipoDb].cursor()
        try:
            # Realiza la consulta SQL solicitada
            cursor.execute("""
                SELECT CONVERT(date, rc.fecha) AS fecha_dia, COUNT(*) AS cantidad
                FROM Registro_Contacto rc
                INNER JOIN report00.[dbo].[Tipificaciones] t ON rc.idrespuesta = t.Idrespuesta
                WHERE CONVERT(date, rc.fecha) >= CONVERT(date, GETDATE() - 5)
                AND t.Tipo = 'CD'
                GROUP BY CONVERT(date, rc.fecha)
                ORDER BY fecha_dia ASC;
            """)

            # Obtiene los resultados
            rows = cursor.fetchall()

            # Prepara los datos en un formato adecuado para la gráfica
            data = [{'fecha': str(row[0]), 'cantidad': row[1]} for row in rows]

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()

        return Response({'ok': True,"Cartera":tipoDb, 'data': data}, status=status.HTTP_200_OK)
   
#ejecutivos 
class ConsultaRutViewAcsa(APIView):   
    def get(self, request, StartDate, EndDate, CampaignName):
        # Validar parámetros
        if not StartDate or not EndDate or not CampaignName:
            return Response({"error": "Todos los parámetros son obligatorios"}, status=400)

        # Convertir fechas a tipo DATE en Python
        try:
            StartDate = datetime.strptime(StartDate, "%Y-%m-%d").strftime('%Y-%m-%d')
            EndDate = datetime.strptime(EndDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        except ValueError:
            return Response({"error": "Formato de fecha incorrecto. Debe ser YYYY-MM-DD"}, status=400)

        CampaignName = str(CampaignName).strip()
        try:
            with connections['vici'].cursor() as cursor:
                query = f"EXEC dbo.proc_resumen_accion_ejecutivo '{StartDate}', '{EndDate}', '{CampaignName}'"

                cursor.execute(query)  # 🔹 Ejecuta sin parámetros

                # Obtener resultados
                columns = [col[0] for col in cursor.description] if cursor.description else []
                data = cursor.fetchall()

            if not data:
                return Response({"message": "No se encontraron resultados."}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        # Convertir resultados a JSON
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)
    
    

class ConsultaWaletsTiemReal(APIView):
    def get(self, request, CampaignName):
        cursor = connections['vici'].cursor()
        try:
            CampaignName = str(CampaignName).strip()
            # Ejecutar el procedimiento almacenado con parámetros
            query = "EXEC proc_resumen_accion_ejecutivo_realtime @CampaignName=%s"
            cursor.execute(query, [CampaignName])

            # Obtener los resultados del procedimiento almacenado
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()

        # Convertir los resultados en JSON
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)

class LastRealTime(APIView):
    def get(self, request):
        try:
            with connections['storage'].cursor() as cursor:
                cursor.execute("""
                    select MAX(fecha) as lastDate from LOGS where nombre like '%realtime%'
                """)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
                
                result_list = [dict(zip(columns, row)) for row in data]
                return Response(result_list)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ReportesSviaIrv(APIView): 
    def get(self, request):
        try:
            with connections['pass'].cursor() as cursor: 
                cursor.execute("""
                    SELECT * FROM vw_total_gestiones_IVR_FONO
                """)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
                
                result_list = [dict(zip(columns, row)) for row in data]
                return Response(result_list)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class CuadraturaSvia(APIView):
    def get(self, request):
        cursor = connections['pass'].cursor()
        try:
            cursor.execute("""
                select * from Cuadratura_Cartera
            """)
            columns = [col[0] for col in cursor.description]  
            data = cursor.fetchall()  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Asegurarse de cerrar el cursor correctamente

        # Convertir los resultados a una lista de diccionarios (clave: nombre de columna)
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)
      
class GeneratorTokenNonExpiring(APIView):  
    def get(self, request):
        user = request.data.get("user")
        password = request.data.get("password")
        try:
            # Generar el token
            token = generate_jwt_token_non_expiring(user, password)
            return Response({"message": "Token generado y almacenado correctamente", "token": token})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class GeneratorTokenExpiring(APIView):  
    def get(self, request):
        user = request.data.get("user")
        password = request.data.get("password")
        try:
            # Generar el token
            token = generate_jwt_token_expiring(user, password)
            return Response({"message": "Token generado y almacenado correctamente", "token": token})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


#ejecucion de monito 

class getMonitoreo(APIView): 
    def get(self, request):
        cursor = connections['config_ssis'].cursor()
        try:
            cursor.execute("""
                select  NombreProceso,FechaInicio, FechaFin,Error,tiempo_segundos,tiempo_minutos,tubo_archivo  from [vista_seguimiento_ssis_Ejecutados]
                WHERE NombreProceso != 'SSIS Extractor de Archivos origenes'
                and  convert(date, FechaInicio) = CONVERT(date,GETDATE())
            """)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        finally:
            cursor.close()
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list)


class gestionAllWallet(APIView):
    def get(self, request, rut):
        cursor = connections['main'].cursor()
        try:
            cursor.execute("""
                  SELECT * FROM fn_asignacion_rut(%s);
            """, [rut])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()  # Cerrar el cursor correctamente
        result_list = [dict(zip(columns, row)) for row in data]
        return Response(result_list, status=status.HTTP_200_OK)