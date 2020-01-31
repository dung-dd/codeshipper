"""codeshipper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from codeshipper import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    # path('accounts/settings/', views.accounts_settings),
    url('^$', include("codeshipper_app.urls")),
    path('cs/', include("codeshipper_app.urls")),
    # url('/', include("codeshipper_app.urls")),

    # fonts
    url(r"a1ecc3b826d01251edddf29c3e4e1e97.woff/?$", views.a1ecc3b826d01251edddf29c3e4e1e97_woff),
    url(r"af7ae505a9eed503f8b8e6982036873e.woff2/?$", views.af7ae505a9eed503f8b8e6982036873e_woff2),
    url(r"fee66e712a8a08eef5805a46892932ad.woff/?$", views.fee66e712a8a08eef5805a46892932ad_woff),
]

handler404 = 'codeshipper.views.handler404'