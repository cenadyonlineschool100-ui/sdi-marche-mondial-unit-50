from django.urls import path
from . import views

app_name = 'app_installer'

urlpatterns = [
    # Views
    path('', views.InstallerMainView.as_view(), name='installer_main'),
    
    # APIs
    path('api/data/', views.GetInstallerDataView.as_view(), name='get_data'),
    path('api/download-apk/', views.DownloadAPKView.as_view(), name='download_apk'),
    path('api/download-apk/<int:apk_id>/', views.DownloadAPKView.as_view(), name='download_apk_specific'),
    path('api/log-installation/', views.log_installation, name='log_installation'),
    path('manifest.json', views.pwa_manifest, name='pwa_manifest'),
    path('service-worker.js', views.service_worker, name='service_worker'),
]
