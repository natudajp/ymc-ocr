from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadForm, SettingForm, UploadPdfForm, PdffileForm
from .models import UploadImage, UploadPdf, Pdffile

from django.http.response import HttpResponse

def main_index(request):
    body ='<a href="/upload_app/">"FAX文字認識システム!"</a>'
    return HttpResponse(body)


def index(request):
    params = {
        'title': '画像のアップロード',
        'upload_form': UploadForm(),
        'id': None,
    }

    if (request.method == 'POST'):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_image = form.save()

            params['id'] = upload_image.id

    #return render(request, 'upload_app/index.html', params)
    return render(request, 'index.html', params)

def preview(request, image_id=0):

    upload_image = get_object_or_404(UploadImage, id=image_id)

    params = {
        'title': '画像の表示',
        'id': upload_image.id,
        'url': upload_image.image.url
    }

    return render(request, 'upload_app/preview.html', params)

def transform(request, image_id=0):

    upload_image = get_object_or_404(UploadImage, id=image_id)

    if (request.method == 'POST'):

        form = SettingForm(request.POST)
        if form.is_valid():
            angle = form.cleaned_data.get('angle')
            gray = form.cleaned_data.get('gray')

            upload_image.transform(angle, gray)

            params = {
                'title': '画像処理',
                'id': upload_image.id,
                'setting_form': form,
                'original_url': upload_image.image.url,
                'result_url': upload_image.result.url
            }

            return render(request, 'upload_app/transform.html', params)


    params = {
        'title': '画像処理',
        'id': upload_image.id,
        'setting_form': SettingForm({'angle':0, 'gray':False}),
        'original_url': upload_image.image.url,
        'result_url': ''
    }

    return render(request, 'upload_app/transform.html', params)

def pdf_index(request):
    pdfs = UploadPdf.objects.all()
    return render(request, 'upload_app/pdf_list.html', {'pdfs': pdfs})

def pdf_upload(request):
    params = {
        'title': 'PDFのアップロード',
        'upload_pdf_form': UploadPdfForm(),
        'pdfname': None,
        'id': None,
    }
    if request.method == 'POST':
        pdfform = UploadPdfForm(request.POST, request.FILES)
        if pdfform.is_valid():
            upload_pdf=pdfform.save()
            params['pdfname']=upload_pdf.pdfdocument
            params['id']=upload_pdf.id


    return render(request, 'upload_app/pdf_upload.html', params)

def pdf2image(request):
    params = {
        'title': 'PDFのアップロード',
        'pdffile_form': PdffileForm(),
        'id': None,
        'pdfname': None,
    }
    #form = PdffileForm()

    if request.method == 'POST':
        form = PdffileForm(request.POST, request.FILES)
        # if form is not valid then form data will be sent back to view to show error message
        if form.is_valid():
            upload_pdf=form.save()
            params['id'] = upload_pdf.id
            params['pdfname']=upload_pdf.pdf
            #return redirect('pdf2image')

    #return render(request, "upload_app/pdf_upload.html", {'form': form})
    return render(request, "upload_app/pdf2img.html",params)

def pdf2image_preview(request, image_id=0):

    upload_image = get_object_or_404(Pdffile, id=image_id)

    params = {
        'title': 'Pdf画像の表示',
        'id': upload_image.id,
        #'url': upload_image.image.url
        'url': upload_image.coverpage.url
    }

    return render(request, 'upload_app/preview.html', params)

# pdf ファイルから画像の取出しと前処理
def pdf2image_ocr(request, image_id=0):

    upload_image = get_object_or_404(Pdffile, id=image_id)

    if (request.method == 'POST'):

        form = SettingForm(request.POST)
        if form.is_valid():
            angle = form.cleaned_data.get('angle')
            gray = form.cleaned_data.get('gray')

            xlsfile=upload_image.pdftransform(angle, gray)

            params = {
                'title': 'PDFファイル画像前処理と文字認識',
                'id': upload_image.id,
                'setting_form': form,
                'original_url': upload_image. coverpage.url,
                'result_url': upload_image.result.url,
                'document': upload_image.text,
                'xlsfile': xlsfile
            }

            return render(request, 'upload_app/pdf2img_ocr.html', params)
    
    params = {
        'title': '文字認識システム',
        'id': upload_image.id,
        'setting_form': SettingForm({'angle':0, 'gray':False}),
        'original_url': upload_image. coverpage.url,
        'result_url': ''
    }

    return render(request, 'upload_app/pdf2img_ocr.html', params)


from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import FormView
from .forms import *
from django.views.decorators.csrf import csrf_exempt
#import json


# Create your views here.

import pytesseract    # ======= > Add
from PIL import Image
'''
try:
    from PIL import Image
except:
    import Image
'''
# Create your views here.

class HomeView(FormView):
    form_class = UploadForm
    template_name = 'upload_app/ocrz_index.html'
    success_url = '/'

    #def form_valid(self, form):
    #    upload = self.request.FILES['file']
    #    print(type(pytesseract.image_to_string(Image.open(upload)))) # =====> add line
   #     return super().form_valid(form)

import os
import pyocr
@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        response_data = {}
        upload = request.FILES['file']
        img=Image.open(upload)
        #'''
        tesseract_path = "C:\Program Files\Tesseract-OCR"
        if tesseract_path not in os.environ["PATH"].split(os.pathsep):
            os.environ["PATH"] += os.pathsep+tesseract_path
            
        pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        tools = pyocr.get_available_tools()

        builder = pyocr.builders.LineBoxBuilder(tesseract_layout=6)
        #document = tools[0].image_to_string(img, lang="jpn", builder=builder)
        document = tools[0].image_to_string(img, lang="jpn")
        #'''
        #builder = pytesseract.builders.LineBoxBuilder(tesseract_layout=6)
        #document= pytesseract.image_to_string(img, lang="jpn")
        #document=document.split('|')
        response_data['document'] = document

        #return JsonResponse(response_data)
        #return HttpResponse(response_data,'ocrz_list.html')
        return HttpResponse(document, 'ocrz_list.html')