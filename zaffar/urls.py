from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.urls')),
    
    path('index.html', TemplateView.as_view(template_name="index.html")),
    
    # path('service-worker.js', TemplateView.as_view(template_name="service-worker.js",
    #                                                content_type='application/javascript'), name='service-worker.js'),
    # path('service-worker.js.map', TemplateView.as_view(template_name="service-worker.js.map",
    #                                                    content_type='application/javascript'), name='service-worker.js.map'),
    # path('manifest.json', TemplateView.as_view(template_name="manifest.json",
    #                                            content_type='application/json'), name='manifest.json'),
    #path('grappelli/', include('grappelli.urls')),
    #path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
   re_path(r'^(?!(api|admin|static|media|manifest.json|service-worker.js|service-worker.js.map).*$)',
            TemplateView.as_view(template_name="index.html")),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)