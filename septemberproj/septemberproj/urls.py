from django.conf.urls import url,include
from django.contrib import admin
from september.views import *
from django.conf.urls.static import static
from django.conf import settings
from september import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register_user, name='register_user'),
    url(r'^login', views.login_from_app, name='login_from_app'),
    url(r'^uploadProductInfo', views.add_product, name='add_product'),
    url(r'^uploadProductImage', views.upload_product_image, name='upload_product_image'),
    url(r'^getMyProductInfo', views.get_products, name='get_products'),
    url(r'^updateProductInfo', views.update_product, name='update_product'),
    url(r'^deleteProductInfo', views.delete_product, name='delete_product'),
    url(r'^getSimilarProductInfo', views.get_similar_products, name='get_similar_products'),
    url(r'^getUserInfo', views.get_member_info, name='get_member_info'),
    url(r'^uploadUserPhoto', views.upload_user_photo, name='upload_user_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
