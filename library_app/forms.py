from django import forms
from django.contrib.auth.models import User
from . import models

class IssuedBookForm(forms.Form):
    isbn2 = forms.ModelChoiceField(queryset = models.Book.objects.all(),
        empty_label = "Book Name [ISBN]", to_field_name = "isbn", label = "Book (Name and ISBN)")
    name2 = forms.ModelChoiceField(queryset = models.Student.objects.all(),
        empty_label = "Name [ID] [Class] [Branch]", to_field_name = "user", label = "Student Details")

    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class': 'form-control'})

class BookForm(forms.Form):
    genre2 = forms.ModelChoiceField(queryset = models.Genre.objects.all(),
        empty_label = "Please choose genre", to_field_name = "genre_name", label = "Book genre")
    language2 = forms.ModelChoiceField(queryset = models.Language.objects.all(),
        empty_label = "Please choose language", to_field_name = "language_name", label = "Book language")

    genre2.widget.attrs.update({'class': 'form-control'})
    language2.widget.attrs.update({'class': 'form-control'})