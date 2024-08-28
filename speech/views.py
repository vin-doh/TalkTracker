from django.shortcuts import render
from .forms import UploadFileForm
import pdfplumber
import docx

# Create your views here.



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('file')
            text_input = request.POST.get('text_input')
            
            if file:
                if file.name.endswith('.docx'):
                    document = docx.Document(file)
                    full_text = [para.text for para in document.paragraphs]
                    speech_text = "\n".join(full_text)
                elif file.name.endswith('.pdf'):
                    text = ""
                    try:
                        with pdfplumber.open(file) as pdf:
                            for page in pdf.pages:
                                text += page.extract_text() or ""
                    except Exception as e:
                        text = f"Error extracting text: {e}"
                    speech_text = text
                elif file.name.endswith('.txt'):
                    speech_text = file.read().decode('utf-8')
                else:
                    speech_text = "Unsupported file format. Please upload a .docx, .pdf, or .txt file."
            elif text_input:
                speech_text = text_input
            else:
                speech_text = "No file or text provided."

            return render(request, 'speech/index.html', {'text': speech_text})
    else:
        form = UploadFileForm()
    return render(request, 'speech/upload.html', {'form': form})
