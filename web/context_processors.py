from django.conf import settings # import the settings file

def show_revistas(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'SHOW_REVISTAS_VIEW': settings.SHOW_REVISTAS_VIEW}