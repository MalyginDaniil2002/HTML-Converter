from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import AddForm, EditForm
from periodic.models import Sheet
from periodic.views import create_file, remove_file
import os
# Create your views here.

@login_required
def account(request):
    return HttpResponseRedirect("./main")

@login_required
def main(request):
    user = request.user
    sheets = Sheet.objects.filter(user=user.id)
    return render(request, "main.html", {'username': user.username, 'sheets': sheets})

@login_required
def add(request):
    warning_msg = "Для добавления нужна публичная ссылка на таблицу!"
    if request.method == "POST":
        addform = AddForm(request.POST)
        if not addform.is_valid():
            return render(request, "change.html", {'form': addform})
        source_link = request.POST.get("source_link")
        if Sheet.objects.filter(source_link=source_link).exists():
            messages.error(request, "Материал по данный ссылке уже загружен!")
            return render(request, "change.html", {'form': addform})
        sheet = Sheet()
        sheet.name = request.POST.get("name")
        sheet.user = User.objects.get(id=request.user.id)
        sheet.source_link = source_link
        sheet.save()
        created_sheet = Sheet.objects.get(source_link=source_link)
        #try:
        work_link = create_file(created_sheet.id, source_link)
        if work_link == "":
            created_sheet.delete()
            messages.error(request, "Данный сервис не поддверживается!")
            return render(request, "change.html", {'form': addform})
        created_sheet.work_link = work_link
        created_sheet.save()
        return HttpResponseRedirect("./")
        '''
        except:
            created_sheet.delete()
            messages.error(request, "Процесс конвертации прошёл неудачно!\nПопробуйте заново.")
            return render(request, "change.html", {'form': addform})
        '''
    else:
        addform = AddForm()
        return render(request, "change.html", {'form': addform})

@login_required
def update(request, sheet_id):
    if Sheet.objects.filter(id=sheet_id, user=request.user.id).exists():
        source_link = Sheet.objects.get(id=sheet_id).source_link
        _ = create_file(sheet_id, source_link)
    return HttpResponseRedirect("..")

@login_required
def edit(request, sheet_id):
    if not Sheet.objects.filter(id=sheet_id, user=request.user.id).exists():
        return HttpResponseRedirect("..")
    if request.method == "POST":
        editform = EditForm(request.POST)
        if not editform.is_valid():
            return render(request, "change.html", {'form': editform})
        sheet = Sheet.objects.get(id=sheet_id)
        sheet.name = request.POST.get("name")
        sheet.save()
        return HttpResponseRedirect("..")
    else:
        editform = EditForm()
        return render(request, "change.html", {'form': editform})

@login_required
def remove(request, sheet_id):
    if Sheet.objects.filter(id=sheet_id, user=request.user.id).exists():
        remove_file(sheet_id)
        Sheet.objects.get(id=sheet_id).delete()
    return HttpResponseRedirect("..")

@login_required
def delete(request):
    user_id = request.user.id
    if Sheet.objects.filter(user=user_id).exists():
        sheets = Sheet.objects.filter(user=user_id)
        for sheet in sheets:
            remove_file(sheet.id)
        sheets.delete()
        User.objects.get(id=user_id).delete()
    return HttpResponseRedirect("../logout")
