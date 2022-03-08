from django.conf import settings
from django.contrib import auth

from .models import UserPref

class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # build themes lookup table
        self.themes = {}
        for item in settings.THEME_CHOICES:
            self.themes[item[0]] = item

        # set default
        self.default_code = self.themes[settings.THEME_DEFAULT][0]
        self.default_css = self.themes[settings.THEME_DEFAULT][2]

    def __call__(self, request):
        # determine theme css to include before the view is processed
        request.theme_code = self.default_code
        request.theme_css = self.default_css
        if request.user.is_authenticated:
            userpref = UserPref.objects.filter(user=request.user)
            if len(userpref) > 0:
                request.theme_code = self.themes[userpref[0].theme][0]
                request.theme_css = self.themes[userpref[0].theme][2]

        # the view (and later middleware) are called.
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
