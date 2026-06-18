from .business_logic import CURRENCY_SYMBOLS, SUPPORTED_CURRENCIES, normalize_currency
from .models import ActivityMenuItem, SiteConfiguration, SystemSettings, PrivateMessage

CURRENCY_DEFAULT = 'USD'

COUNTRY_CODE_TO_CURRENCY = {
    'HT': 'HTG',
    'DO': 'DOP',
    'US': 'USD',
    'FR': 'EUR',
}

LANGUAGE_TO_CURRENCY = {
    'ht': 'HTG',
    'es-do': 'DOP',
    'en-us': 'USD',
    'fr': 'EUR',
}


def detect_currency_from_request(request):
    country_code = request.META.get('HTTP_CF_IPCOUNTRY') or request.META.get('GEOIP_COUNTRY_CODE')
    if country_code:
        country_code = country_code.strip().upper()
        if country_code in COUNTRY_CODE_TO_CURRENCY:
            return COUNTRY_CODE_TO_CURRENCY[country_code]

    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if not accept_language:
        return None

    accept_language = accept_language.lower()
    for lang, currency in LANGUAGE_TO_CURRENCY.items():
        if lang in accept_language:
            return currency

    if 'us' in accept_language:
        return 'USD'
    if 'fr' in accept_language:
        return 'EUR'
    return None


def currency_context(request):
    currency = request.session.get('currency')
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile and not currency:
            currency = profile.preferred_currency

    if not currency:
        currency = detect_currency_from_request(request) or CURRENCY_DEFAULT

    currency = normalize_currency(currency)
    if currency not in SUPPORTED_CURRENCIES:
        currency = CURRENCY_DEFAULT

    return {
        'current_currency': currency,
        'current_currency_symbol': CURRENCY_SYMBOLS.get(currency, currency),
        'currency_choices': [(code, code) for code in SUPPORTED_CURRENCIES],
        'price_conversion_note': 'Prix indicatif – paiement final selon la méthode choisie',
    }


from django.db import OperationalError


def site_config_context(request):
    configs = {}
    try:
        for config in SiteConfiguration.objects.all():
            configs[config.config_type] = config
    except OperationalError:
        # La table n'existe peut-être pas encore en base pendant la migration
        pass
    return {'site_configs': configs}


def activity_menu_context(request):
    default_items = [
        {
            'title': 'Mes Cours',
            'url': '#',
            'icon_class': 'fa-solid fa-graduation-cap',
            'description': 'Voir les formations achetées ou suivies.\nAccéder aux cours en ligne et aux vidéos.',
        },
        {
            'title': 'Studio de Beauté',
            'url': '/profile/studio-beaute/',
            'icon_class': 'fa-solid fa-spa',
            'description': 'Voir les services de beauté disponibles.\nRéserver ou consulter les offres.',
        },
        {
            'title': '🏠 Immobilier / Maison à Louer',
            'url': '/immobilier/',
            'icon_class': 'fa-solid fa-house',
            'description': 'Voir les maisons et appartements disponibles.\nConsulter les détails et contacter le propriétaire.',
        },
        {
            'title': 'Boutique',
            'url': '#',
            'icon_class': 'fa-solid fa-store',
            'description': 'Voir les produits et services publiés.',
        },
        {
            'title': 'Mes Commandes',
            'url': '#',
            'icon_class': 'fa-solid fa-box-open',
            'description': 'Consulter l\'historique des achats.',
        },
        {
            'title': 'Mes Messages',
            'url': '#',
            'icon_class': 'fa-solid fa-envelope',
            'description': 'Accéder aux messages privés.',
        },
        {
            'title': 'Mes Transactions',
            'url': '#',
            'icon_class': 'fa-solid fa-money-bill-transfer',
            'description': 'Consulter les dépôts, retraits et transferts.',
        },
        {
            'title': 'SDI Transfer à l’étranger',
            'url': '/profile/transfer/',
            'icon_class': 'fa-solid fa-globe',
            'description': 'Transfert international sécurisé. Le bénéficiaire reçoit son agent à domicile en USD.',
        },
        {
            'title': 'SDI Sol',
            'url': '#',
            'icon_class': 'fa-solid fa-sun',
            'description': 'Accéder au module SDI Sol.',
        },
    ]
    try:
        items = list(ActivityMenuItem.objects.filter(is_active=True).order_by('order').values('title', 'url', 'description', 'icon_class'))
        if not items:
            items = default_items
    except Exception:
        items = default_items

    return {'activity_menu_items': items}


def private_chat_context(request):
    unread_count = 0
    if request.user.is_authenticated:
        try:
            unread_count = PrivateMessage.objects.filter(receiver=request.user, is_read=False).count()
        except Exception:
            unread_count = 0
    return {'private_unread_message_count': unread_count}


def system_settings_context(request):
    settings_obj = None
    try:
        settings_obj, created = SystemSettings.objects.get_or_create(pk=1)
    except OperationalError:
        settings_obj = None
    return {'system_settings': settings_obj}


import json


def theme_context(request):
    """Context processor pour injecter les données de thème utilisateur dans tous les templates."""
    theme_name = 'blue-mirror'
    theme_settings = {}
    
    try:
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile:
                theme_name = profile.theme_name or 'blue-mirror'
                theme_settings = profile.theme_settings or {}
        else:
            cookie_theme_name = request.COOKIES.get('ui_theme_name')
            cookie_theme_settings = request.COOKIES.get('ui_theme_settings')
            if cookie_theme_name:
                theme_name = cookie_theme_name
            if cookie_theme_settings:
                try:
                    parsed_settings = json.loads(cookie_theme_settings)
                    if isinstance(parsed_settings, dict):
                        theme_settings = parsed_settings
                except (json.JSONDecodeError, TypeError):
                    pass
    except Exception:
        # En cas d'erreur, utiliser les valeurs par défaut
        pass
    
    return {
        'user_theme_name': theme_name,
        'user_theme_settings': theme_settings,
    }


def announcement_context(request):
    """
    Add active announcements to template context
    """
    try:
        from django.utils import timezone
        from marketplace.models import AdminAnnouncement
        
        # Get active announcements
        now = timezone.now()
        announcements = AdminAnnouncement.objects.filter(
            is_active=True,
            status='active'
        ).order_by('-is_priority', '-created_at')
        
        # Filter by date if start/end dates are set
        active_announcements = []
        for announcement in announcements:
            if announcement.start_date and announcement.start_date > now:
                continue
            if announcement.end_date and announcement.end_date < now:
                continue
            active_announcements.append(announcement)
        
        # Get priority announcement if exists
        priority_announcement = None
        for announcement in active_announcements:
            if announcement.is_priority:
                priority_announcement = announcement
                break
        
        # Get first announcement if no priority
        active_announcement = priority_announcement or (active_announcements[0] if active_announcements else None)
        
        return {
            'active_announcement': active_announcement,
            'all_active_announcements': active_announcements,
        }
    except Exception as e:
        # Log error but don't break the site
        print(f"Error in announcement_context: {e}")
        return {
            'active_announcement': None,
            'all_active_announcements': [],
        }


