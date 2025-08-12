from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if email:
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
                sociallogin.state['process'] = 'login'
            except User.DoesNotExist:
                pass

    def get_login_redirect_url(self, request):
        return 'blog-home'
