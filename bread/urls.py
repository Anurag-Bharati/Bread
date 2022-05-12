from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from bread import views

urlpatterns = [
    path('', include('home.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('auth/', include('users.urls')),
    path('manage/', include('manage.urls')),
    path('home-page/', include('customer.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
