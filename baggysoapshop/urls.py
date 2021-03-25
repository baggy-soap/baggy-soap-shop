"""baggysoapshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.flatpages import views
from django.urls import include, path
from django.apps import apps


# from paypal.express.dashboard.app import application as paypal_application

urlpatterns = [
    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.
    path('admin/', admin.site.urls),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml/', TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml")),
    path('i18n/', include('django.conf.urls.i18n')),
    path('checkout/paypal/', include('paypal.express.urls')),
    path('dashboard/paypal/express/', apps.get_app_config("express_dashboard").urls),

    path('', include(apps.get_app_config('oscar').urls[0])),
    
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('benefits/', views.flatpage, {'url': '/benefits/'}, name='benefits'),
    path('delivery/', views.flatpage, {'url': '/delivery/'}, name='delivery'),
    path('faq/', views.flatpage, {'url': '/faq/'}, name='faq'),
    path('products/', views.flatpage, {'url': '/products/'}, name='products'),
    path('contact/', views.flatpage, {'url': '/contact/'}, name='contact'),
    path('tandc/', views.flatpage, {'url': '/tandc/'}, name='tandc'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
