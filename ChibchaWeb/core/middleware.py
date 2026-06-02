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
    """Apply stored language preference when the session has no explicit choice."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.utils import translation

        user = getattr(request, 'user', None)
        if not user or not getattr(user, 'is_authenticated', False):
            return self.get_response(request)

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

        return self.get_response(request)
