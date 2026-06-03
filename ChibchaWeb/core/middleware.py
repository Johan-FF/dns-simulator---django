"""Project middleware helpers."""

from Clientes.models import Cliente


class PersistUserLanguageMiddleware:
    """Save language choice to the client profile after Django set_language."""

    SET_LANGUAGE_PATH = '/i18n/setlang/'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.method == 'POST'
            and request.path.rstrip('/') == self.SET_LANGUAGE_PATH.rstrip('/')
            and request.user.is_authenticated
        ):
            language = request.POST.get('language', '').strip()
            if language:
                Cliente.objects.filter(user=request.user).update(preferred_language=language)
        return response


class ActivateUserLanguageMiddleware:
    """Apply stored language preference when the session has no explicit choice and force language prefix redirects."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.utils import translation
        from django.conf import settings
        from django.urls import is_valid_path
        from django.shortcuts import redirect

        # 1. Apply user preference if logged in
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            language_session_key = getattr(translation, 'LANGUAGE_SESSION_KEY', '_language')
            if language_session_key not in request.session:
                try:
                    cliente = Cliente.objects.get(user=request.user)
                    if cliente.preferred_language:
                        translation.activate(cliente.preferred_language)
                        request.LANGUAGE_CODE = cliente.preferred_language
                except Cliente.DoesNotExist:
                    pass
            else:
                try:
                    cliente = Cliente.objects.get(user=user)
                    lang = request.session.get(language_session_key)
                    if lang and cliente.preferred_language != lang:
                        cliente.preferred_language = lang
                        cliente.save(update_fields=['preferred_language'])
                except Cliente.DoesNotExist:
                    pass

        # 2. If active language is not the default language, redirect prefixless URLs to prefixed versions
        language = translation.get_language()
        if language and language != settings.LANGUAGE_CODE:
            language_from_path = translation.get_language_from_path(request.path_info)
            if not language_from_path:
                language_path = '/%s%s' % (language, request.path_info)
                urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
                if is_valid_path(language_path, urlconf):
                    query_string = request.META.get('QUERY_STRING', '')
                    target_url = language_path
                    if query_string:
                        target_url += '?' + query_string
                    return redirect(target_url)

        return self.get_response(request)
