from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.template.response import TemplateResponse
from django.core.files.storage import default_storage
from django.conf import settings
from pathlib import Path
import json
import logging
import json as json_lib
import zipfile
from user_agents import parse

from .models import APKVersion, PWAConfig, InstallationLog

logger = logging.getLogger(__name__)


class InstallerMainView(View):
    """Vue principale pour afficher l'interface d'installation"""
    
    def get(self, request):
        # Récupérer la dernière version active d'APK
        latest_apk = APKVersion.objects.filter(is_active=True).first()
        
        # Récupérer la configuration PWA
        pwa_config = PWAConfig.objects.first()
        
        context = {
            'latest_apk': latest_apk,
            'pwa_config': pwa_config,
        }
        
        return TemplateResponse(request, 'app_installer/installer_modal.html', context)


class GetInstallerDataView(View):
    """API pour récupérer les données d'installation"""
    
    def get(self, request):
        latest_apk = APKVersion.objects.filter(is_active=True).first()
        pwa_config = PWAConfig.objects.first()
        
        data = {
            'apk': None,
            'pwa': None,
        }
        
        if latest_apk:
            data['apk'] = {
                'version': latest_apk.version_number,
                'min_android_version': latest_apk.min_android_version,
                'file_size_mb': latest_apk.file_size_mb,
                'download_url': latest_apk.apk_file.url,
                'release_notes': latest_apk.release_notes,
            }
        
        if pwa_config and pwa_config.is_enabled:
            data['pwa'] = {
                'app_name': pwa_config.app_name,
                'short_name': pwa_config.short_name,
                'icon_192': pwa_config.icon_192.url if pwa_config.icon_192 else None,
                'icon_512': pwa_config.icon_512.url if pwa_config.icon_512 else None,
                'theme_color': pwa_config.theme_color,
                'background_color': pwa_config.background_color,
            }
        
        return JsonResponse(data)


class DownloadAPKView(View):
    """Télécharger l'APK et enregistrer l'installation"""
    
    def get(self, request, apk_id=None):
        if apk_id:
            apk = get_object_or_404(APKVersion, id=apk_id, is_active=True)
        else:
            apk = APKVersion.objects.filter(is_active=True).first()
            if not apk:
                return JsonResponse({'error': 'No active APK available'}, status=404)
        
        # Enregistrer le téléchargement
        apk.download_count += 1
        apk.save(update_fields=['download_count'])
        
        # Enregistrer l'installation dans les logs
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)
        
        InstallationLog.objects.create(
            installation_type='apk',
            user_agent=user_agent_string,
            device_type='mobile',
            os_type=str(user_agent.os),
            browser=str(user_agent.browser),
            status='pending',
            ip_address=self.get_client_ip(request),
            apk_version=apk,
            session_id=request.session.session_key or 'anonymous'
        )
        
        # Retourner le fichier APK
        if apk.apk_file:
            try:
                apk_file = apk.apk_file
                apk_path = getattr(apk_file, 'path', None)
                if apk_path:
                    is_valid_apk = zipfile.is_zipfile(apk_path)
                else:
                    is_valid_apk = False
                if not is_valid_apk:
                    return JsonResponse({'error': 'APK file is invalid or corrupt'}, status=500)
            except Exception as e:
                logger.error(f"APK validation failed: {e}")
                return JsonResponse({'error': 'APK file is invalid or corrupt', 'details': str(e)}, status=500)

            response = FileResponse(apk.apk_file.open('rb'), content_type='application/vnd.android.package-archive')
            response['Content-Disposition'] = f'attachment; filename="sdi_market_v{apk.version_number}.apk"'
            return response
        
        return JsonResponse({'error': 'APK file not found'}, status=404)
    
    @staticmethod
    def get_client_ip(request):
        """Obtenir l'adresse IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


@csrf_exempt
@require_http_methods(["POST"])
def log_installation(request):
    """Enregistrer une installation PWA"""
    try:
        data = json.loads(request.body)
        
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)
        
        # Déterminer le type d'appareil
        if user_agent.is_mobile:
            device_type = 'mobile'
        elif user_agent.is_tablet:
            device_type = 'tablet'
        else:
            device_type = 'desktop'
        
        InstallationLog.objects.create(
            installation_type='pwa',
            user_agent=user_agent_string,
            device_type=device_type,
            os_type=str(user_agent.os),
            browser=str(user_agent.browser),
            status='success',
            ip_address=get_client_ip(request),
            session_id=request.session.session_key or 'anonymous'
        )
        
        return JsonResponse({'success': True, 'message': 'Installation logged'})
    except Exception as e:
        logger.error(f"Error logging installation: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def get_client_ip(request):
    """Obtenir l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_http_methods(["GET"])
def pwa_manifest(request):
    """Générer le manifest.json pour la PWA"""
    pwa_config = PWAConfig.objects.first()
    
    if not pwa_config or not pwa_config.is_enabled:
        return JsonResponse({'error': 'PWA not configured'}, status=404)
    
    manifest = {
        'name': pwa_config.app_name,
        'short_name': pwa_config.short_name,
        'description': pwa_config.description,
        'start_url': pwa_config.start_url,
        'scope': pwa_config.scope,
        'display': 'standalone',
        'orientation': pwa_config.orientation,
        'theme_color': pwa_config.theme_color,
        'background_color': pwa_config.background_color,
        'icons': [
            {
                'src': pwa_config.icon_192.url if pwa_config.icon_192 else '',
                'sizes': '192x192',
                'type': 'image/png',
                'purpose': 'any'
            },
            {
                'src': pwa_config.icon_512.url if pwa_config.icon_512 else '',
                'sizes': '512x512',
                'type': 'image/png',
                'purpose': 'any maskable'
            }
        ]
    }
    
    if pwa_config.splash_screen:
        manifest['screenshots'] = [
            {
                'src': pwa_config.splash_screen.url,
                'sizes': '1920x1080',
                'type': 'image/png',
                'form_factor': 'wide'
            }
        ]
    
    return JsonResponse(manifest)


@require_http_methods(["GET"])
def service_worker(request):
    """Servir le service worker depuis la racine pour prendre en charge l'installation PWA."""
    sw_path = Path(settings.BASE_DIR) / 'app_installer' / 'static' / 'service-worker.js'
    if not sw_path.exists():
        return HttpResponse('Service worker introuvable.', status=404)

    with sw_path.open('rb') as sw_file:
        response = HttpResponse(sw_file.read(), content_type='application/javascript')
        response['Service-Worker-Allowed'] = '/'
        return response
