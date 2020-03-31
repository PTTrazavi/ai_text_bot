from django.urls import include, path
from . import views

# 用來串接callback主程式
urlpatterns = [
    path('validationEng/', views.textvalidationEng, name='text_validationEng'),
    path('resultEng/', views.resultEng, name='resultEng'),
    path('inquiryEng/', views.inquiryEng, name='inquiryEng'),
    path('lineEng/', views.lineEng, name='lineEng'),
    path('pdfEng/', views.pdfEng, name='pdfEng'),
    path('AlistEng/', views.textupload_listEng.as_view(), name='textupload_listEng'),
    path('AlistEng/<int:pk>', views.textupload_detailEng.as_view(), name='textupload_detailEng'),
    path('IlistEng/', views.inquiry_listEng.as_view(), name='inquiry_listEng'),
    path('IlistEng/<int:pk>', views.inquiry_detailEng.as_view(), name='inquiry_detailEng'),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
