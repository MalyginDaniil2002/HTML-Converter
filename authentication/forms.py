from django import forms


class SignInForm(forms.Form):
    login    = forms.CharField(label='Логин', max_length=50)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    login           = forms.CharField(label='Логин', max_length=50)
    email           = forms.EmailField(label='Эл. почта', max_length=200)
    main_password   = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    check_password  = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)


    def clean(self):
        cleaned_data    = super().clean()
        main_password   = cleaned_data.get("main_password")
        check_password  = cleaned_data.get("check_password")

        if main_password != check_password:
            msg = "Повторно введеный пароль не совпадает с основным!"
            self.add_error("check_password", msg)
