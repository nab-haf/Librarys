# main/context_processors.py

def global_context(request):
    return {
        "user_permissions": request.user.get_all_permissions() if request.user.is_authenticated else [],
        "current_app": request.resolver_match.app_name if request.resolver_match else None,
    }
