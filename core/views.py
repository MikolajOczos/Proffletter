import os
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from .models import files, contactforms
import pymupdf
import io
from openai import OpenAI


def index(request): ##main index page, sending documents
    return render(request, 'index.html')

def contact(request): ##contact page
    return render(request, "contact.html")




def upload_file(request): ## uploading a file at main index page and counting it
    if request.method == "POST" and "document" in request.FILES:
        uploaded_file = request.FILES["document"]
        
        if not (uploaded_file.name.endswith('.pdf') or uploaded_file.name.endswith('.docx') or uploaded_file.name.endswith(".txt")):
            
            return render(request, "index_fail.html")
        
            
        else:
            size_check = check_size(request, uploaded_file)  ## checking size, possibly returning to index_fail
            if size_check != True:  ## <-------
                return size_check
            if uploaded_file.name.endswith(".txt"):
                counter = 0
                uploaded_file.seek(0)
                content = uploaded_file.read().decode('utf-8')
                for x in content:
                    counter = counter + 1
                fs = FileSystemStorage() ## saving file to storage, then creating a object in a db##
                saved_path = fs.save(uploaded_file.name, uploaded_file)
                files.objects.create(
                        filename = uploaded_file.name,
                        file = saved_path,
                        characters = counter
                    )    
                return render(request, "index.html", {
                    'uploaded_file_name': uploaded_file.name,
                    'character_count': counter
                })
            elif uploaded_file.name.endswith('.docx') or uploaded_file.name.endswith('.pdf'):
                if size_check != True:  ##<------
                    return size_check
                uploaded_file.seek(0)
                file_content = uploaded_file.read()
                file_stream = io.BytesIO(file_content)
                doc = pymupdf.open(stream=file_stream)
                content = 0
                counter = 0
                for page in doc:
                    text = list(page.get_text())
                    for x in text:
                        counter = counter + 1
                    fs = FileSystemStorage() ## saving file to storage, then creating a object in a db##
                    saved_path = fs.save(uploaded_file.name, uploaded_file)
                    files.objects.create(
                        filename = uploaded_file.name,
                        file = saved_path,
                        characters = counter
                    )
                return render(request, "index.html", {
                    'uploaded_file_name': uploaded_file.name,
                    'character_count': counter
                })
             
def check_size(request, uploaded_file): ## Checking the size of upoloaded file
    max_uploaded_file_size = 5 * 1024 * 1024
    if uploaded_file.size >= max_uploaded_file_size:
        return render(request, "index_fail.html")
    return True

                
def clear_doc(request): ## clearing the document sent at the main index page
    if request.method ==  "GET":
        render(request, "index.html")
    return render(request, "index.html")

def indextype(request):
    return render(request, "indextype.html")

def sendcontact(request): ## sending the forms to the db
    if request.method == "POST":
        email = request.POST.get("email") 
        message = request.POST.get("message")
        contactforms.objects.create(
            email = email,
            formcontent = message,
        )
    return render(request, "contact.html")

def officializer(request):
    return render(request, "officializer.html")        
                
def upload_official(request):
    if request.method == "POST":
        client = OpenAI(api_key=" your own ") 
        usertext = request.POST.get("inputText")
        readyprompt = f"""
        You are an assistant that rewrites text into a more official, classy, 
        professional, and elegant tone. Keep the meaning, but improve clarity, 
        structure, and formality.

        Rewrite the following text:

        "{usertext}"
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You rewrite text into a more official and elegant form."},
                {"role": "user", "content": readyprompt}
            ]
        )


        output_text = response.choices[0].message.content


        clean = output_text.strip()

        if clean.startswith("{") and clean.endswith("}"):
            clean = clean[1:-1].strip()

        return render(request, "officializer.html", {"output": clean})


           

   
