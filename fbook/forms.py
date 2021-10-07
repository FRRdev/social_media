from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError

from .models import BookUser, Post, Message
from django.contrib.auth import password_validation


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронный почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз для проверки')
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.widgets.DateInput(attrs={'type': 'date', }))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()  # отослат польз письмо с треб актвации
        return user

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        errors = {}
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1'] != \
                self.cleaned_data['password2']:
            errors['password2'] = ValidationError('Введенные пароли не совпадают',
                                                  code='password_mismatch')
            raise ValidationError(errors)
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            try:
                user = BookUser.objects.get(email=email)
                if user:
                    errors['email'] = ValidationError('Текущий email уже занят!',
                                                      code='password_mismatch')
                    raise ValidationError(errors)
            except BookUser.DoesNotExist:
                pass
        return self.cleaned_data

    class Meta:
        model = BookUser
        fields = (
            'first_name', 'last_name', 'email', 'password1', 'password2', 'image', 'phone', 'date_of_birth', 'city',
            'about_me')


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок')

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {'user': forms.HiddenInput, 'create_at': forms.HiddenInput}


class SendMessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows': 4, 'placeholder': 'Введите сообщение'}),
                              label='')

    class Meta:
        model = Message
        exclude = ('is_active',)
        widgets = {'chat': forms.HiddenInput, 'author': forms.HiddenInput}
