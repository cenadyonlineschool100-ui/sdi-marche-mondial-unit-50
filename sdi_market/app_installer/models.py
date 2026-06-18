from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os


class APKVersion(models.Model):
    """Modèle pour gérer les versions d'application Android (APK)"""
    version_number = models.CharField(max_length=20, unique=True, help_text="Ex: 1.0.0")
    apk_file = models.FileField(
        upload_to='apk_files/',
        validators=[FileExtensionValidator(allowed_extensions=['apk'])]
    )
    release_notes = models.TextField(blank=True, help_text="Notes de version (changements, améliorations)")
    is_active = models.BooleanField(default=True, help_text="Version disponible au téléchargement")
    min_android_version = models.CharField(
        max_length=10,
        default="5.0",
        help_text="Version minimale d'Android requise"
    )
    file_size = models.BigIntegerField(help_text="Taille du fichier en bytes", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    download_count = models.IntegerField(default=0, help_text="Nombre de téléchargements")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Version APK"
        verbose_name_plural = "Versions APK"

    def __str__(self):
        return f"APK v{self.version_number}"

    def save(self, *args, **kwargs):
        if self.apk_file:
            self.file_size = self.apk_file.size
        super().save(*args, **kwargs)

    @property
    def file_size_mb(self):
        """Convertir la taille en MB"""
        return round(self.file_size / (1024 * 1024), 2)


class PWAConfig(models.Model):
    """Modèle pour configurer la Progressive Web App (PWA)"""
    app_name = models.CharField(max_length=100, default="SDI Marché")
    short_name = models.CharField(max_length=12, default="SDI Market")
    description = models.TextField(default="Plateforme e-commerce mondiale")
    
    # Icônes PWA
    icon_192 = models.ImageField(
        upload_to='pwa_assets/',
        help_text="Icône PWA 192x192px"
    )
    icon_512 = models.ImageField(
        upload_to='pwa_assets/',
        help_text="Icône PWA 512x512px"
    )
    
    # Écran de démarrage
    splash_screen = models.ImageField(
        upload_to='pwa_assets/',
        blank=True,
        null=True,
        help_text="Écran de démarrage (1920x1080px recommandé)"
    )
    
    # Couleurs
    theme_color = models.CharField(
        max_length=7,
        default="#0066FF",
        help_text="Couleur principale (format #RRGGBB)"
    )
    background_color = models.CharField(
        max_length=7,
        default="#FFFFFF",
        help_text="Couleur de fond (format #RRGGBB)"
    )
    
    # Configuration
    is_enabled = models.BooleanField(default=True)
    start_url = models.CharField(max_length=200, default="/")
    scope = models.CharField(max_length=200, default="/")
    orientation = models.CharField(
        max_length=20,
        choices=[('portrait', 'Portrait'), ('landscape', 'Landscape'), ('any', 'Any')],
        default='portrait'
    )
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration PWA"
        verbose_name_plural = "Configuration PWA"

    def __str__(self):
        return f"PWA Config - {self.app_name}"


class InstallationLog(models.Model):
    """Modèle pour enregistrer les installations"""
    INSTALLATION_TYPE_CHOICES = [
        ('apk', 'APK'),
        ('pwa', 'PWA'),
    ]

    installation_type = models.CharField(max_length=10, choices=INSTALLATION_TYPE_CHOICES)
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(
        max_length=20,
        choices=[('mobile', 'Mobile'), ('tablet', 'Tablet'), ('desktop', 'Desktop')],
        default='mobile'
    )
    os_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="iOS, Android, Windows, macOS, Linux, etc."
    )
    browser = models.CharField(max_length=50, blank=True, help_text="Chrome, Safari, Firefox, etc.")
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')],
        default='pending'
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    apk_version = models.ForeignKey(
        APKVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='installations'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Installation Log"
        verbose_name_plural = "Installation Logs"
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['installation_type']),
        ]

    def __str__(self):
        return f"{self.installation_type.upper()} - {self.device_type} - {self.timestamp}"
