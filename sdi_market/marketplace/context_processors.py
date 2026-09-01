"""
Marketplace context processors with graceful fallbacks for deployment
"""


def navigation_context(request):
    """Add navigation configuration to context"""
    return {
        'marketplace_inactivity_timeout_seconds': 600,
    }


def currency_context(request):
    """Add currency information to context"""
    return {
        'current_currency': 'USD',
        'current_currency_symbol': '$',
        'currency_choices': [
            ('USD', 'USD'),
            ('EUR', 'EUR'),
            ('HTG', 'HTG'),
            ('DOP', 'DOP'),
        ],
        'price_conversion_note': 'Prix indicatif – paiement final selon la méthode choisie',
    }


def site_config_context(request):
    """Add site configuration to context"""
    return {'site_configs': {}}


def activity_menu_context(request):
    """Add activity menu items to context"""
    return {'activity_menu_items': []}


def private_chat_context(request):
    """Add private chat information to context"""
    return {'unread_message_count': 0}


def announcement_context(request):
    """Add admin announcements to context"""
    return {'admin_announcements': []}


def site_banner_context(request):
    """Add site banner information to context"""
    return {'site_banner': None}


def system_settings_context(request):
    """Provide a safe fallback for the system settings singleton.

    This avoids crashes when the database has not been migrated yet or the
    singleton record is not present.
    """
    return {'system_settings': None}
