from django import forms


class AddForm(forms.Form):
    name        = forms.CharField(label='Имя таблицы', max_length=100)
    source_link = forms.CharField(label='Ссылка на источник')

class EditForm(forms.Form):
    name = forms.CharField(label='Имя таблицы', max_length=100)
