from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

"""
Page Not found  
"""
handler404 = 'dashboard.views.error_404_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include('products.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('api/knox/auth/', include('knox.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('', include("accounts.urls")),
    path('policy/', include("policy.urls")),
    path('b2bmanagement/', include("b2bmanagement.urls")),
    path('b2bproduct/', include("b2bproduct.urls")),
    path("claim/", include("claim.urls")),
    path('api/', include("b2bmanagement.api_urls")),
    path('api/', include("claim.api_urls")),
    path('api/', include("b2bproduct.api_urls")),
    path('api/', include("dashboard.api_urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = 'InsureTech B2B'
admin.site.site_title = 'InsureTech B2B'
admin.site.index_title = 'InsureTech B2B'