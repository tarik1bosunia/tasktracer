from django.utils import timezone
import pytz

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # You can store user's timezone in their profile
            user_tz = request.user.profile.timezone  # Adjust based on your user model
            if user_tz:
                timezone.activate(pytz.timezone(user_tz))
            else:
                timezone.deactivate()
        else:
            timezone.deactivate()
        return self.get_response(request)