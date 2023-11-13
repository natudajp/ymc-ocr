from django import forms
from .models import UploadImage, UploadPdf, Pdffile

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['image']

class SettingForm(forms.Form):
    angle = forms.IntegerField()
    gray = forms.BooleanField(required=False)

class UploadPdfForm(forms.ModelForm):
    class Meta:
        model = UploadPdf
        fields = ('description', 'pdfdocument', )

class PdffileForm(forms.ModelForm):
    class Meta:
        model = Pdffile
        fields = (
            'pdf',
            'filename',
            'pagenumforcover',
        )

class UploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        'id': 'file_id'
    }
    )
    )