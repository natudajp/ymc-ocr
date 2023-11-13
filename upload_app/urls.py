
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pdf2image, name='index'),
    # pdfファイルアップロード
    path('pdf/', views.pdf_index, name='pdf_list'),
    path('pdf_upload/', views.pdf_upload, name='pdf_upload'),
    # pdfからimageへの変換
    path('pdf2image/', views.pdf2image, name='pdf2img'),
    path('pdfpreview/<int:image_id>/', views.pdf2image_preview, name='pdfpreview'),
    path('pdfocr/<int:image_id>/', views.pdf2image_ocr, name='ocr'),
    
    path('ocrz/', views.HomeView.as_view()),
    path('process_image/', views.process_image, name='process_image') # New line
]