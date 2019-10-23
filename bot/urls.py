from django.urls import include, path
from . import views

# 用來串接callback主程式
urlpatterns = [
    path('validation/', views.textvalidation, name='text_validation'),
    path('result/', views.result, name='result'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('line/', views.line, name='line'),
    path('pdf/', views.pdf, name='pdf'),
    path('Alist/', views.textupload_list.as_view(), name='textupload_list'),
    path('Alist/<int:pk>', views.textupload_detail.as_view(), name='textupload_detail'),
    path('Ilist/', views.inquiry_list.as_view(), name='inquiry_list'),
    path('Ilist/<int:pk>', views.inquiry_detail.as_view(), name='inquiry_detail'),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
