from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.views.generic import TemplateView, RedirectView

# class RootView(TemplateView):
#     template_name = 'root.html'

urlpatterns = [
    path('', RedirectView.as_view(
        pattern_name='instagram:post_list',
    ), name='root'),
    path('admin/', admin.site.urls),
    path('blog1/', include('blog1.urls')),
    path('instagram/', include('instagram.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# settings.MEDIA_URL
# settings.MEDIA_ROOT

    import debug_toolbar
    urlpatterns += [
        path('__debug__/',include(debug_toolbar.urls)),
    ]
