from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import PDFUploadForm
from pdf2docx import Converter

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            fs = FileSystemStorage()
            filename = fs.save(pdf_file.name, pdf_file)
            pdf_path = fs.url(filename)

            # Convert PDF to Word
            docx_filename = filename.replace('.pdf', '.docx')
            converter = Converter(fs.path(filename))
            converter.convert(docx_filename, start=0, end=None)
            converter.close()

            return render(request, 'converter/result.html', {'docx_file': docx_filename})

    else:
        form = PDFUploadForm()
    return render(request, 'converter/upload.html', {'form': form})
