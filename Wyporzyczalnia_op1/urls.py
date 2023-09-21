"""URL configuration for Wyporzyczalnia_app

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
from Wyporzyczalnia_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('uslugi/', views.uslugi, name='uslugi'),
    path('onas/', views.onas, name='onas'),
    path('machinery/', views.machinery_list, name='machinery_list'),
    path('machinery/<int:machinery_id>/', views.machinery_detail_view, name='machinery_detail'),
    path('rental/', views.rental_list, name='rental_list'),
    path('rental/<int:rental_id>/', views.rental_detail, name='rental_detail'),
    path('company/<int:company_id>/', views.company_detail, name='company_detail'),
    path('add_rating/<int:company_id>/', views.add_rating, name='add_rating'),
    path('add_comment/<int:company_id>/', views.add_comment, name='add_comment'),
    path('login_user/', views.LoginUser.as_view(), name='login_user'),
    path('logout_user/', views.LogoutUser.as_view(), name='logout_user'),
    path('add_user/', views.AddUser.as_view(), name='add_user'),
    path('add_machinery/', views.add_machinery, name='add_machinery'),
    path('add_company/', views.add_company, name='add_company'),
    path('rental/<int:rental_id>/add_delivery/', views.add_delivery, name='add_delivery'),
    path('machinery/<int:machinery_id>/add_comment/', views.add_comment, name='add_comment'),
]