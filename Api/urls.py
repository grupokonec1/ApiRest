
# Api/urls.py

from django.urls import path
from .views import CombinedPhonesView,AllWalleteMonedero,getCuotasAvo,CompromisosRotosEjecutivosPass,DiaryAllWalletPass,DiaryAllWallet,CompromisosRotosEjecutivoAllWallet,InhabilitadosAcsa,getChequesAcsa,GetGrupoFacturacionAcsa,ConveniosAcsa,PagoAutomaticoAcsa,getDescuentoSvia,InsertDireccionWalletSvia,getAllDirecionClientSvia,BoletasPagadasSvia,getNameExecutiveForWallet,getRecuperoEjecutivos,getPagosEjecutivosWallet,getUsersPassWallet,CompromisosRotosAllWallet,BoletasPagadas,MonederoAllWallet,PagosWallet,TotalMontoCompromiso,showCdToSupervisionPass,CompromisosRotosPass,dicomSvia,getGestionRutWallets,showCdToSupervision,getAllPhoneClient,getUsersAllWallet,getAllEmailClient,getCallAutorizados,InsertEmailAllWallets,InsertPhonoAllWallets,InsertarRegistroContactoAutorizaLlamado,SendMailingView,DescuentoAllWallet,DescuentoPass,Refinanciaciones,ListarGestionesAllWalletPass,RefinanciacionesPass,TipificacionesAll,ListarTipificacionesApi,InsertarNewEmailPass,InsertarNewPhonoPass,ContactByRUTPass,ConsultaRutViewPass,InsertarRegistroContactoPass,NASAudioDownload,NASAudioSearchAll,NASAudioSearch,SendSMSNG,SmsStatusAPIView,GetCallAgainAll,InsertaCallAgain,getDescuentoAvo,ConsultaViewPatenteAvo,GetDataDiaryAPIView,ListarGestionesAllWallet,ContactByRUTGlobal,ListarTipificacionesCondeza,InsertarNewEmailCondeza,InsertarNewPhonoCondeza,ListarGestionesCondeza,InsertarRegistroContactoCondeza,ConsultaRutViewCondeza,ConsultaRutUserView,ListarPpuAcsa,ListarDescuentoAcsa,InsertarNewPhonoSvia,InsertarNewEmailSvia,InsertarNewEmailAvn,InsertarNewPhonoAvn,InsertarNewPhonoAvo,InsertarNewEmailAvo,InsertarNewEmailAcsa,InsertarNewPhonoAcsa,ListarBotetaAcsa,InsertarNewEmailGlobal,InsertarNewPhonoGlobal,ConsultaRutViewGlobal,ContactByRUTAvo,ConsultaRutViewAcsa,InsertarRegistroContactoAcsa,ListarTipificacionesRepoort,ConsultaRutViewAvo,InsertarRegistroContactoAvo,InsertarRegistroContactoGlobal,InsertarRegistroContactoVnort,ListarPagosAcsa,InsertarRegistroContacto,ContactByRUT,ConsultaRutView,CarterTotalesByRUT,ConsultaRutViewVnorte,ContactByRUTvnort

urlpatterns = [
    path('insertar-registro-contacto-svia/', InsertarRegistroContacto.as_view(), name='insertar-registro-contacto-svia'),
    path('consulta-rut-svia/<str:rutdv>/', ConsultaRutView.as_view(), name='consulta-rut'),
    path('boletas-svia/<str:rutdv>/', ContactByRUT.as_view(), name='contact-by-rut'),
    path('cartera-svia/<str:rutdv>/', ContactByRUT.as_view(), name='contact-by-rut'),
    path('cartera-totales-svia/<str:rutdv>/', CarterTotalesByRUT.as_view(), name='contact-by-rut'),
    path('insertar-NewEmail-svia/', InsertarNewEmailSvia.as_view(), name='insertar-newEmail'),
    path('insertar-NewPhono-svia/', InsertarNewPhonoSvia.as_view(), name='insertar-newPhono'),
    path('descuento-svia/<str:rut>/', getDescuentoSvia.as_view(), name='contact-patente-avo'),
   
    path('consulta-rut-avn/<str:rutdv>/', ConsultaRutViewVnorte.as_view(), name='consulta-rutvnort'),
    path('cartera-avn/<str:rut>/', ContactByRUTvnort.as_view(), name='contact-by-rut-vnort'),
    path('insertar-registro-contacto-avn/', InsertarRegistroContactoVnort.as_view(), name='insertar-registro-contacto'),
    path('insertar-NewEmail-avn/', InsertarNewEmailAvn.as_view(), name='insertar-newEmail'),
    path('insertar-NewPhono-avn/', InsertarNewPhonoAvn.as_view(), name='insertar-newPhono'),


    path('insertar-registro-contacto-global/', InsertarRegistroContactoGlobal.as_view(), name='insertar-registro-contacto'),
    path('consulta-rut-global/<str:rutdv>/', ConsultaRutViewGlobal.as_view(), name='consulta-rut-global'),
    path('boletas-global/<str:rutdv>/', ContactByRUTGlobal.as_view(), name='contact-by-rut-global'),
    path('cartera-global/<str:rutdv>/', ContactByRUTGlobal.as_view(), name='contact-by-rut-global'),
    path('insertar-NewEmail-global/', InsertarNewEmailGlobal.as_view(), name='insertar-newEmail'),
    path('insertar-NewPhono-global/', InsertarNewPhonoGlobal.as_view(), name='insertar-newPhono'),


#cambiar todas los que dicen cartera

    path('insertar-registro-contacto-acsa/', InsertarRegistroContactoAcsa.as_view(), name='insertar-registro-contacto_i'),
    path('consulta-rut-acsa/<str:rutdv>/', ConsultaRutViewAcsa.as_view(), name='consulta-rutvacsa'),
    path('pagos-acsa/', ListarPagosAcsa.as_view(), name='listar-pagos-acsa'),
    path('descuento-acsa/<str:rutdv>/', ListarDescuentoAcsa.as_view(), name='listar-pagos-acsa'),
    path('ppu-acsa/<str:rutdv>/', ListarPpuAcsa.as_view(), name='listar-pagos-acsa'),
    path('boletas-acsa/<str:rutdv>/', ListarBotetaAcsa.as_view(), name='listar-botetas-acsa'),#eliminar cuando cambie de crm
    path('boleta-acsa/<str:rutdv>/', ListarBotetaAcsa.as_view(), name='listar-botetas-acsa'),#eliminar cuando cambie de crm
    path('pago-automatico-acsa/<str:ic>/', PagoAutomaticoAcsa.as_view(), name='listar-botetas-acsa'),
    path('Convenios-acsa/<str:rut>/', ConveniosAcsa.as_view(), name='listar-botetas-acsa'),
    path('grupo-facturacion-acsa/<str:ic>/', GetGrupoFacturacionAcsa.as_view(), name='listar-botetas-acsa'),
    path('cheques-acsa/<str:rut>/', getChequesAcsa.as_view(), name='listar-botetas-acsa'),
    path('inhabilita-acsa/<str:ic>/', InhabilitadosAcsa.as_view(), name='listar-botetas-acsa'),



    path('cartera-acsa/<str:rutdv>/', ListarBotetaAcsa.as_view(), name='listar-botetas-acsa'),
    path('insertar-NewEmail-acsa/', InsertarNewEmailAcsa.as_view(), name='insertar-newEmail'),
    path('insertar-NewPhono-acsa/', InsertarNewPhonoAcsa.as_view(), name='insertar-newPhono'),



    
    
    path('insertar-registro-contacto-avo/', InsertarRegistroContactoAvo.as_view(), name='insertar-registro-contacto'),
    path('consulta-rut-avo/<str:rutdv>/', ConsultaRutViewAvo.as_view(), name='consulta-rutvavo'),
    path('boletas-avo/<str:rutdv>/', ContactByRUTAvo.as_view(), name='contact-by-rut-avo'),
    path('cartera-avo/<str:rutdv>/', ContactByRUTAvo.as_view(), name='contact-by-rut-avo'),
    path('insertar-NewEmail-avo/', InsertarNewEmailAvo.as_view(), name='insertar-newEmail'),
    path('insertar-NewPhono-avo/', InsertarNewPhonoAvo.as_view(), name='insertar-newPhono'),
    path('patente-avo/<str:rutdv>/', ConsultaViewPatenteAvo.as_view(), name='contact-patente-avo'),
    path('descuento-avo/<str:rutdv>/', getDescuentoAvo.as_view(), name='contact-patente-avo'),
    path('cuotas/<str:rut>/', getCuotasAvo.as_view(), name='contact-patente-avo'),

#condeza
    path('consulta-rut-condeza/<str:rutdv>/', ConsultaRutViewCondeza.as_view(), name='contact-by-rut-condeza'),
    path('insertar-registro-contacto-condeza/', InsertarRegistroContactoCondeza.as_view(), name='insertar-registro-contacto-condeza'),
    path('listar-gestiones-condeza/<str:rutdv>/', ListarGestionesCondeza.as_view(), name='listar-pagos-acsa'),
    path('insertar-NewEmail-condeza/', InsertarNewEmailCondeza.as_view(), name='insertar-newEmail-condeza'),
    path('insertar-NewPhono-condeza/', InsertarNewPhonoCondeza.as_view(), name='insertar-newPhono-condeza'),

#general
    path('getUserWalletPass/<str:idclient>/', getUsersPassWallet.as_view(), name='get-users-pass'),
    path('getUserAllWallets/<str:tipo>/<str:idclient>/',getUsersAllWallet.as_view(), name='get-users-pass'),
#revisar
    path('monederoAllWallet/<str:tipo>/', MonederoAllWallet.as_view(), name='dicom-pass'),
        
    
    path('insertAllEmailWallet/', InsertEmailAllWallets.as_view(), name='grupo-facturacion'),
    path('insertAllPhoneWallet/', InsertPhonoAllWallets.as_view(), name='insert-phono'),
    path('insertDireccionWalletSvia/', InsertDireccionWalletSvia.as_view(), name='insert-phono'),

    path('showAllEmailClient/<str:tipo>/<str:rut>/', getAllEmailClient.as_view(), name='get-email'),
    path('showAllPhoneClient/<str:tipo>/<str:rut>/', getAllPhoneClient.as_view(), name='get-phono'),
    path('showAllDireccionClientSvia/<str:rut>/', getAllDirecionClientSvia.as_view(), name='get-phono'),

    
    path('user/<str:rutdv>/', ConsultaRutUserView.as_view(), name='listar-tipificaciones-report'),
    path('tipificaciones-report/', ListarTipificacionesRepoort.as_view(), name='listar-tipificaciones-report'),
    path('tipificaciones-api/', ListarTipificacionesApi.as_view(), name='listar-tipificaciones-report'),
    path('tipificaciones-condeza/', ListarTipificacionesCondeza.as_view(), name='listar-tipificaciones-condeza'),
    path('listar-gestiones/<str:tipo>/<str:rutdv>/', ListarGestionesAllWallet.as_view(), name='listar-pagos-acsa'),
    path('listar-gestiones-pss/<str:tipo>/<str:rutdv>/', ListarGestionesAllWalletPass.as_view(), name='listar-pagos-acsa'),
    
    #revisar agenda urgent---
    path('listar-wallet/<str:tipo>/<str:ruteje>/<int:idclient>/', GetDataDiaryAPIView.as_view(), name='listar-all-diary'),
    path('listar-agendaWallets/<str:tipo>/<str:ruteje>/', DiaryAllWallet.as_view(), name='listar-all-diary'),
    
    
    
    
    #crm agenda 
    path('getCdAllExecutive/<str:tipo>/<str:ruteje>/', showCdToSupervision.as_view(), name='listar-all-diary'),
    
    path('getAgendaExecutivePass/<str:ruteje>/', showCdToSupervisionPass.as_view(), name='listar-all-diary'),
    #crm getGestiones compromiso roto
    path('getAllGestionesRutsRoto/<str:dbName>/<str:rut>/', getGestionRutWallets.as_view(), name='listar-all-diary'),
    
    #revisar agenda urgent------
    path('listar-agendaPass/<str:ruteje>/', DiaryAllWalletPass.as_view(), name='listar-all-diary'),
    
    
    
    
    #boletas pagados
    path('boletasPagados-pass/<str:rut>/', BoletasPagadas.as_view(), name='monedero-all-wallet'),
    path('boletasPagados-svia/<str:rut>/', BoletasPagadasSvia.as_view(), name='monedero-all-wallet'),

    #revisar si se utiliza 
    path('listar-callAuthorize/<str:ruteje>/<str:tipo>/', getCallAutorizados.as_view(), name='listar-all-diary'),


    path('insert-callAgain/', InsertaCallAgain.as_view(), name='callAgain'),
    path('insert-authorizesCall/', InsertarRegistroContactoAutorizaLlamado.as_view(), name='callAgain'),
    path('Allcombinedphones/', CombinedPhonesView, name='combined-phones'),
    path('tipificaciones/', TipificacionesAll.as_view(), name='tipificaciones'),
    path('getCallAgainAll/<str:prefix>/', GetCallAgainAll.as_view(), name='grupo-facturacion'),
    path('sms-status/', SmsStatusAPIView.as_view(), name='sms_status'),
    path('sms-send/', SendSMSNG.as_view(), name='sms_send'),
    path('send-mailing/', SendMailingView.as_view(), name='sms_send'),
    path('search-audios-celular/', NASAudioSearch.as_view(), name='search_audios'),
    path('search-audios-old/', NASAudioSearchAll.as_view(), name='search_audios'),
    path('download-audios-celular/', NASAudioDownload.as_view(), name='download_audios'),
    

#pass
#POR ELIMINAR 
    path('refinanciaciones-pass/<str:rut>/', RefinanciacionesPass.as_view(), name='contact-by-rut-condeza'),
    path('refinanciaciones/<str:rut>/', Refinanciaciones.as_view(), name='contact-by-rut-condeza'),
    path('dicomSvia/<str:rut>/', dicomSvia.as_view(), name='dicom-pass'),
    
#compromisos rotos
    path('compromisosRotoPass/', CompromisosRotosPass.as_view(), name='dicom-pass'),
    
    #revisar compromisos
    path('compromisosRotoAllWallet/<str:tipo>/', CompromisosRotosAllWallet.as_view(), name='dicom-pass'),
    path('compromisosRotoEjecutivosPass/<str:ruteje>/', CompromisosRotosEjecutivosPass.as_view(), name='dicom-pass'),
    path('compromisosAllEjecutivosWallet/<str:tipo>/<str:ruteje>/', CompromisosRotosEjecutivoAllWallet.as_view(), name='dicom-pass'),
    

    path('consulta-rut-pass/<str:rutdv>/', ConsultaRutViewPass.as_view(), name='consulta-rutvpass'),
    path('insertar-registro-contacto-pass/', InsertarRegistroContactoPass.as_view(), name='insertar-registro-contacto_i'),
    path('boletas-pass/<str:customer_nid>/', ContactByRUTPass.as_view(), name='contact-by-rut-pass'),
    path('cartera-pass/<str:customer_nid>/', ContactByRUTPass.as_view(), name='contact-by-rut-pass'),
    path('insertar-NewEmail-pass/', InsertarNewEmailPass.as_view(), name='insertar-newEmail-condeza'),
    path('insertar-NewPhono-pass/', InsertarNewPhonoPass.as_view(), name='insertar-newPhono-condeza'),
    #POR ELIMINAR 
    path('descuento-pass/<str:rut>/', DescuentoPass.as_view(), name='contact-by-rut-condeza'),
    path('descuento-wallet/pass/<str:rut>/', DescuentoPass.as_view(), name='contact-by-rut-condeza'),
    path('descuento-wallet/<str:tipo>/<str:rut>/', DescuentoAllWallet.as_view(), name='listar-pagos-acsa'),

   #monedero all wallet
   
    path('monederoWallets/<str:tipo>/', AllWalleteMonedero.as_view(), name='monedero-all-wallet'),
    
    #here Monedero Pagos
    path('pagosTotales/<str:tipo>/', PagosWallet.as_view(), name='monedero-all-wallet'),
    path('pagosTotalesCompromiso/<str:tipo>/', TotalMontoCompromiso.as_view(), name='monedero-all-wallet'),
    
    
    #nombre de ejecutivos for k3
    path('nameExecutivesAllWallets/<str:tipo>/', getNameExecutiveForWallet.as_view(), name='dicom-pass'),
    path('getPagosEjecutivos/<str:ruteje>/<str:tipo>/', getPagosEjecutivosWallet.as_view(), name='dicom-pass'),
    path('getRecuperoEjecutivo/<str:tipo>/', getRecuperoEjecutivos.as_view(), name='dicom-pass'),





]
