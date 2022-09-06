from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView

admin.site.site_title = "Online-Shop Administration"
admin.site.site_header = "Online-Shop Administration"

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.shop.urls')),
    path('api/v1/', include('user.urls')),
    # path('api/v1/', include('apps.shop.urls')),
    prefix_default_language=False
)

handler404 = 'online-shop.views.handler404'
handler500 = 'online-shop.views.handler500'

if settings.DEBUG:
    urlpatterns += [
        # Testing 404 and 500 error pages
        path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
        path('500/', TemplateView.as_view(template_name='500.html'), name='500'),
    ]

    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
    ]

    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
