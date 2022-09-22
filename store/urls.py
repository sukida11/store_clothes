from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'store'

urlpatterns = [
    path('', IndexPageView.as_view(), name='startpage'),
    path('catalog/', ProductsView.as_view(), name='catalog'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_user, name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)