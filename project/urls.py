from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rest/', include('rest_framework.urls')),
    path('api/auth/', include('accounts.urls')),
    path('', include('product.urls')),
    path('api/', include('order.urls')),
    path('api/', include('cart.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)