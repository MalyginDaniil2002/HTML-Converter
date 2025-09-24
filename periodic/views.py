#from django.shortcuts import render
from django.apps import AppConfig
from django.conf import settings
from django.http import FileResponse, HttpResponse
from onedrivedownloader import download
from urllib.parse import urlencode
#from .models import Sheet
import os, pandas, requests, time
from django.core.signals import request_started
from django.dispatch import receiver
import threading

from html_converter.settings import MEDIA_ROOT


def show(request, file_name):
    file_path = f"{settings.MEDIA_ROOT}/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        return HttpResponse("Такого файла нет")

def create_html(file_name, excel_name, html_name):
    table = pandas.read_excel(excel_name)
    html_output = table.to_html(index=False)
    with open(html_name, 'w') as file:
        file.write(html_output)
    os.remove(excel_name)
    return f'{settings.CSRF_TRUSTED_ORIGINS[0]}/show/{file_name}.html'

def create_file(sheet_id, source_link):
    work_link = ""
    file_name = f"file{sheet_id}"
    excel_name = f"{settings.MEDIA_ROOT}/{file_name}.xlsx"
    html_name = f"{settings.MEDIA_ROOT}/{file_name}.html"
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)
    if "docs.google.com" in source_link:
        work_link = f"https://docs.google.com/spreadsheets/d/{source_link.split('/')[5]}/gviz/tq?tqx=out:html"
    elif "1drv.ms" in source_link:
        download(source_link, excel_name)
        work_link = create_html(file_name, excel_name, html_name)
    elif "disk.yandex.ru" in source_link:
        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        final_url = base_url + urlencode(dict(public_key=source_link))
        response = requests.get(final_url)
        download_url = response.json()['href']
        download_response = requests.get(download_url)
        with open(excel_name, 'wb') as file:
            file.write(download_response.content)
        work_link = create_html(file_name, excel_name, html_name)
    return work_link

def remove_file(sheet_id):
    path = f'{settings.MEDIA_ROOT}/file{sheet_id}.html'
    if os.path.exists(path):
        os.remove(path)

'''
class PeriodicTask(AppConfig):
    name = "views.PeriodicTask"

    @staticmethod
    def ready(self):
        from .models import Sheet
        print("Проверка")
        thread = threading.Thread(target=update_files(1))
        thread.daemon = True
        thread.start()
'''
