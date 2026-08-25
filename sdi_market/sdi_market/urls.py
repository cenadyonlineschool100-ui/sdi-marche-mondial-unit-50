from django.contrib import admin
from django.urls import path, include, re_path
from app_installer import views as app_installer_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from marketplace.views import admin_add_money, admin_add_agent, manage_delivery_assignments
from django.urls import include as dj_include

urlpatterns = [
    path('service-worker.js', app_installer_views.service_worker, name='service_worker_root'),
    path('', include('marketplace.urls')),
    path('beauty-studios/', include('beauty.urls')),
    path('installer/', include('app_installer.urls')),
    path('admin/add-money/', admin_add_money, name='admin_add_money'),
    path('admin/add-agent/', admin_add_agent, name='admin_add_agent'),
    path('admin/manage-delivery-assignments/', manage_delivery_assignments, name='admin_manage_delivery_assignments'),
    path('admin/', admin.site.urls),
    path('savings/', include('savings.urls')),
]

# Servir les fichiers médias pour l'instance locale
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except Exception:
        # debug_toolbar not installed
        pass