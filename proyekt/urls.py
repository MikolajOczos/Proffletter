
from django.contrib import admin
from django.urls import path
from core.views import index, contact, upload_file, clear_doc, indextype, sendcontact, upload_official, officializer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path("contact/", contact, name="contact"),
    path("upload/", upload_file, name = "upload_file"),
    path("clear/", clear_doc, name="clear_doc"),
    path("type/", indextype, name = "indextype" ),
    path("s/", sendcontact, name = "sendcontact"),
    path("officializer+s/", upload_official, name="upload_official"),
    path("officializer/", officializer, name = "officializer")

]

