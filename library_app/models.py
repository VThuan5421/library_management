from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.urls import reverse # Used to generate urls by reversing the URL patterns

# Create your models here.
class Genre(models.Model):
    genre_name = models.CharField(max_length = 200, help_text = "Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.genre_name
    # __str__ method is used to override default string returned by an object
class Language(models.Model):
    language_name = models.CharField(max_length = 200, help_text = "Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.language_name

# book relation that has 2 foreign key author language
# book relation can contain multiple genre so we have used manytomanyfiled
class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    isbn = models.CharField('ISBN', max_length = 13, unique = True, help_text = '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text = "Select a genre for this book")
    language = models.ForeignKey(Language, on_delete = models.SET_NULL, null = True)
    description = models.TextField(null = True, blank = True)
    total_copies = models.IntegerField()
    book_available = models.IntegerField(default = 0)
    image = models.ImageField(upload_to = 'book_image', blank = True)

    def get_absolute_url(self):
        return reverse('book_detail', args = [str(self.id)])

    def get_slice_title(self):
        return str(self.title)[:15]

    def __str__(self):
        return str(self.title) + " [" + str(self.isbn) + "]"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    fullname = models.CharField(max_length = 100)
    classroom = models.CharField(max_length = 10)
    branch = models.CharField(max_length = 100)
    roll_no = models.CharField(max_length = 15, unique = True)
    phone = models.CharField(max_length = 11, blank = True)
    total_books_due = models.IntegerField(default = 0)
    image = models.ImageField(blank = True, upload_to = 'student_image')
    

    def __str__(self):
        return str(self.user) + " [" + str(self.roll_no) + "][" +str(self.fullname) + "][" + str(self.classroom) + "][" + str(self.branch) + "]"

def expiry():
    return datetime.today() + timedelta(days = 14)

# relation containing info about Borrowed books
# it has foreign key book and studetn for referencing book and student
# roll_no is used for indentifing students
# if a book is returned than corresponding tuple is deleted from database
class IssuedBook(models.Model):
    student_id = models.CharField(max_length = 15, blank = True)
    isbn = models.CharField(max_length = 13)
    issued_date = models.DateField(auto_now = True)
    expiry_date = models.DateField(default = expiry)
    
    
    """
    student = Student.objects.get(id = student_id)
    book = Book.objects.filter(isbn = isbn)
    def __str__(self):
        return self.student.roll_no +" - " + self.student.user.get_full_name + " borrows " + self.book.roll_no + " - " + self.book.title
    """
# The 1 version of borrower a book.
class IssuedBook1(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    issued_date = models.DateField(auto_now = True)
    expiry_date = models.DateField(default = expiry)

    def __str__(self):
        return "[" + str(self.student.roll_no) +" - "+ str(self.student.fullname) + "] borrowed " + str(self.book.title)


