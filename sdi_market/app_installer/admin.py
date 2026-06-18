from django.contrib import admin
from django.utils.html import format_html
from .models import APKVersion, PWAConfig, InstallationLog


@admin.register(APKVersion)
class APKVersionAdmin(admin.ModelAdmin):
    list_display = [
        'version_number',
        'file_size_mb_display',
        'is_active_display',
        'download_count',
        'created_at_display'
    ]
    list_filter = ['is_active', 'created_at', 'min_android_version']
    search_fields = ['version_number', 'release_notes']
    readonly_fields = ['file_size', 'created_at', 'updated_at', 'download_count', 'file_preview']
    fieldsets = (
        ('Version Information', {
            'fields': ('version_number', 'apk_file', 'file_preview', 'file_size', 'min_android_version')
        }),
        ('Status', {
            'fields': ('is_active', 'download_count')
        }),
        ('Release Notes', {
            'fields': ('release_notes',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def file_size_mb_display(self, obj):
        return f"{obj.file_size_mb} MB"
    file_size_mb_display.short_description = "File Size"

    def is_active_display(self, obj):
        color = 'green' if obj.is_active else 'red'
        status = 'Active' if obj.is_active else 'Inactive'
        return format_html(
            '<span style="color: {};">●</span> {}',
            color,
            status
        )
    is_active_display.short_description = "Status"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    created_at_display.short_description = "Created"

    def file_preview(self, obj):
        if obj.apk_file:
            return format_html(
                '<a href="{}" target="_blank" style="padding: 8px 12px; background-color: #0066FF; '
                'color: white; text-decoration: none; border-radius: 4px;">Download APK</a>',
                obj.apk_file.url
            )
        return "No file uploaded"
    file_preview.short_description = "APK File"

    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} APK(s) marked as active.")
    mark_as_active.short_description = "Mark selected APKs as active"

    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} APK(s) marked as inactive.")
    mark_as_inactive.short_description = "Mark selected APKs as inactive"


@admin.register(PWAConfig)
class PWAConfigAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'short_name', 'is_enabled_display', 'theme_color_display', 'updated_at']
    readonly_fields = ['updated_at', 'config_preview']
    fieldsets = (
        ('Application Names', {
            'fields': ('app_name', 'short_name', 'description')
        }),
        ('Icons & Splash Screen', {
            'fields': ('icon_192', 'icon_512', 'splash_screen')
        }),
        ('Colors', {
            'fields': ('theme_color', 'background_color')
        }),
        ('PWA Configuration', {
            'fields': ('is_enabled', 'start_url', 'scope', 'orientation')
        }),
        ('Preview', {
            'fields': ('config_preview',)
        }),
        ('Last Updated', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def is_enabled_display(self, obj):
        color = 'green' if obj.is_enabled else 'red'
        status = 'Enabled' if obj.is_enabled else 'Disabled'
        return format_html(
            '<span style="color: {};">●</span> {}',
            color,
            status
        )
    is_enabled_display.short_description = "Status"

    def theme_color_display(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; '
            'background-color: {}; border-radius: 3px; border: 1px solid #ccc;"></span> {}',
            obj.theme_color,
            obj.theme_color
        )
    theme_color_display.short_description = "Theme Color"

    def config_preview(self, obj):
        preview = f"""
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px;">
            <h4>PWA Configuration Preview</h4>
            <p><strong>App Name:</strong> {obj.app_name}</p>
            <p><strong>Short Name:</strong> {obj.short_name}</p>
            <p><strong>Theme Color:</strong> {obj.theme_color}</p>
            <p><strong>Background Color:</strong> {obj.background_color}</p>
            <p><strong>Orientation:</strong> {obj.get_orientation_display()}</p>
            <p><strong>Start URL:</strong> {obj.start_url}</p>
        </div>
        """
        return format_html(preview)
    config_preview.short_description = "Preview"

    def has_add_permission(self, request):
        # Only one PWA config allowed
        return not PWAConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


@admin.register(InstallationLog)
class InstallationLogAdmin(admin.ModelAdmin):
    list_display = [
        'installation_type_display',
        'device_type_display',
        'os_type',
        'status_display',
        'timestamp_display'
    ]
    list_filter = [
        'installation_type',
        'device_type',
        'status',
        'os_type',
        'timestamp'
    ]
    search_fields = ['session_id', 'ip_address', 'os_type', 'browser']
    readonly_fields = [
        'installation_type',
        'user_agent',
        'device_type',
        'os_type',
        'browser',
        'status',
        'ip_address',
        'apk_version',
        'timestamp',
        'session_id'
    ]
    date_hierarchy = 'timestamp'

    def installation_type_display(self, obj):
        color = '#0066FF' if obj.installation_type == 'pwa' else '#FF6600'
        icon = '🌐' if obj.installation_type == 'pwa' else '📱'
        return format_html(
            '<span style="color: {};">{} {}</span>',
            color,
            icon,
            obj.get_installation_type_display()
        )
    installation_type_display.short_description = "Type"

    def device_type_display(self, obj):
        icons = {
            'mobile': '📱',
            'tablet': '📱',
            'desktop': '💻'
        }
        return f"{icons.get(obj.device_type, '?')} {obj.get_device_type_display()}"
    device_type_display.short_description = "Device"

    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'success': 'green',
            'failed': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">●</span> {}',
            color,
            obj.get_status_display()
        )
    status_display.short_description = "Status"

    def timestamp_display(self, obj):
        return obj.timestamp.strftime('%d/%m/%Y %H:%M:%S')
    timestamp_display.short_description = "Time"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
