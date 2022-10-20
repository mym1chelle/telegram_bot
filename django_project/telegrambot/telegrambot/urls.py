from django.contrib import admin
from django.urls import path
from django_project.telegrambot.telegrambot import settings
from django.conf.urls.static import static

from django_project.telegrambot.usermanage.views import send_message

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send_message/', send_message, name='send_message'),
]


if settings.DEBUG: # она стоит True когда ведется режим разработки проекта
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)