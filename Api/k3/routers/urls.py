from django.urls import include, path
from Api.k3.controllers.views import ContactosDc,proxyGmini_view,CuadraturaSvia,getMonitoreo,GeneratorTokenExpiring,GeneratorTokenNonExpiring,ReportesSviaIrv,LastRealTime,nonAgentApi,ConsultaWaletsTiemReal,ConsultaRutViewAcsa,DeadCallInsertView,VerifyOrRefreshTokenView,deleteUsersWalletModule,InsertWallets,InsertModules,getPermissionsModule,getPermissionsWallet,InsertOrUpdatePermissionsWalletView,InsertOrUpdatePermissionsModuleView,GetModulesUserForRut,getAreas,getModules,getWallet,getRoles,RegisterUserView,getModulesUser,getLoginUser,getAllUsers,ListNASFilesRRHHView,PreviewNASFileView,ListSMBFilesRrrHhView,ListSMBFilesUniqueView,DownloadNASFileView,ListNASFilesView,ListFilesServerView,CleanFolderSFTPView,getUsersAsigned,InsertFileSFTPView,UploadSFTPFileView,CreateSFTPDirectoryView,insert_logs,RecordingAllWalletView,RecordingSviaView,download_file,proxy_view,get_audio_files,InformeGestionToday,generar_reporte_externo,generar_reporte_interno
from Api.k3.middlewares.validateJWT import ValidateTokenView

urlpatterns = [
    path('get-user-asigned-sftp/', getUsersAsigned.as_view(), name='get_user_asigned'),
    path('GestionesRporExterno/', generar_reporte_externo, name='gestiones-report-externo'),
    path('GestionesRporInternas/', generar_reporte_interno, name='gestiones-report-internas'),
    path('GestionesRporToday/', InformeGestionToday.as_view(), name='gestiones-report-internas'),
    path('SearchRecording-svia/', InformeGestionToday.as_view(), name='gestiones-report-internas'),
    path('get-audio-files/', get_audio_files, name='get-audio-files'),
    path('download-file/<str:file_name>/', download_file, name='download-file'),
    path('Recording-svia/', RecordingSviaView.as_view(), name='recording-svia'),
    path('recordingAllWallet/', RecordingAllWalletView.as_view(), name='recording-global'),
    path('insert-logs/', insert_logs, name='insert_logs'),

    path('list-nas/', ListNASFilesView.as_view(), name='list-file'),
    path('list-nas-RRHH/', ListNASFilesRRHHView.as_view(), name='list-file'),
    path('create-folder/', CreateSFTPDirectoryView.as_view(), name='list-file'),
    path('upload-file/', UploadSFTPFileView.as_view(), name='list-file'),
    path('download-file-nas/', DownloadNASFileView.as_view(), name='download_sftp_file'),
    path('preview-file-nas/', PreviewNASFileView.as_view(), name='preview_nas_file'),
    path('list-files-unique/', ListSMBFilesUniqueView.as_view(), name='listar-archivos'),
    path('list-files-RRHH/', ListSMBFilesRrrHhView.as_view(), name='listar-archivos'),
   
    path('insert-files-server/', InsertFileSFTPView.as_view(), name='insert_logs'),
    path('clear-files/', CleanFolderSFTPView.as_view(), name='insert_logs'),
    path('list-files-server/', ListFilesServerView.as_view(), name='list-server'),

    path('proxy/', proxy_view, name='proxy'),
    
    path('proxy-gmini/', proxyGmini_view, name='proxy'),
    path('non-agent-api/', nonAgentApi, name='proxy'),
    path('dead-call/', DeadCallInsertView.as_view(), name='dead_call'),
    
    path('getAllUsers/', getAllUsers.as_view(), name='getAllUsers'),
    path('getOneUser/', getLoginUser.as_view(), name='getOneUser'),
    path('getModulesUser/', getModulesUser.as_view(), name='getOneUser'),
    path('setRegister/', RegisterUserView.as_view(), name='getOneUser'),
    path('validate-token/', ValidateTokenView.as_view(), name='validate_token'),
    path('getRoles/', getRoles.as_view(), name='getAllUsers'),
    path('getWallet/', getWallet.as_view(), name='getAllUsers'),
    path('getModules/', getModules.as_view(), name='getAllUsers'),
    path('getAreas/', getAreas.as_view(), name='getAllUsers'),
    path('getModulesUserForRut/', GetModulesUserForRut.as_view(), name='getOneUser'),
    path('insertModules/', InsertOrUpdatePermissionsModuleView.as_view(), name='insertModule'),
    path('insertWallet/', InsertOrUpdatePermissionsWalletView.as_view(), name='insertModule'),
    path('PermissionsWallet/', getPermissionsWallet.as_view(), name='getAllUsers'),
    path('PermissionsModule/', getPermissionsModule.as_view(), name='getAllUsers'),
    path('insertModulesdb/', InsertModules.as_view(), name='insertModule'),
    path('insertWalletdb/', InsertWallets.as_view(), name='insertWallet'),
    path('deleteWalletModuleUsers/', deleteUsersWalletModule.as_view(), name='insertWallet'),
    path('ContactoDc/', ContactosDc.as_view(), name='contactoDc'),
    path('token-verify-refresh/', VerifyOrRefreshTokenView.as_view(), name='verify_or_refresh_token'),
    
    path('resumen-ejecutivo/<str:StartDate>/<str:EndDate>/<str:CampaignName>/', ConsultaRutViewAcsa.as_view(), name='dicom-pass'),
    path('resumen-ejecutivo-realtime/<str:CampaignName>/', ConsultaWaletsTiemReal.as_view(), name='dicom-pass'),
    path('realtime/', LastRealTime.as_view(), name='realtime'),
    path('reportesSvia/', ReportesSviaIrv.as_view(), name='realtime'),
    path('cuadratura-pass/', CuadraturaSvia.as_view(), name='realtime'),
    
    #token
    path('tokenNoExpiring/',GeneratorTokenNonExpiring.as_view(), name='token'),
    path('token/',GeneratorTokenExpiring.as_view(), name='token'),    
    
    #monitoreo
    path('monitoreo-ejecucion/',getMonitoreo.as_view(), name='getMonitoreo'),
    
    #todos las gestiones de la cartera falta
    # path('gestiones-wallet/<str:rut>/', gestionAllWallet.as_view(), name='gestiones-all-wallet'),
    


]
