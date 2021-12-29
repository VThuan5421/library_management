from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import IssuedBookForm
from django.contrib.auth import authenticate, login, logout
from .import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.db.models import Q
import re

# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_login(request):
    if request.user.is_authenticated or request.user.is_superuser:
        return redirect("/logout")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user= authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse('<h1 class = "text-center">Your are not an admin</h1>')
        else:
            alert = True
            return render(request, "admin_login.html", {'alert': alert})
    return render(request, "admin_login.html")
"""
@login_required
def add_book(request):
    form = forms.BookForm()
    if not request.user.is_superuser:
        return redirect('index')
    if request.method == "POST":
        form = forms.BookForm({'genre_name': request.POST['genre2'], 'language_name': request.POST['language2']})
        if form.is_valid():
            
            obj = models.Book()
            obj.title = request.POST['title']
            obj.author = request.POST['author']
            obj.isbn = request.POST['isbn']
            obj.genre = request.POST['genre2']
            obj.language = request.POST['language2']
            obj.description = request.POST['description']
            obj.total_copies = request.POST['total_copy']
            if request.FILES['image'] is not None:
                obj.image = request.FILES['image']
            else:
                obj.image = ""
            
            obj.save()
            alert = True
            return render(request, "add_book.html", {'alert': alert})
        else:
            return HttpResponse("None")
    return render(request, 'add_book.html', {'form': form})
"""
@login_required
def add_book(request):
    form = forms.BookForm()
    if not request.user.is_superuser:
        return redirect('/')
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        genre_check = Genre.objects.filter(genre_name = request.POST['genre2'])
        language_check = Language.objects.get(language_name = request.POST['language2'])
        language = language_check
        description = request.POST['description']
        total_copies = request.POST['total_copy']
        image = request.FILES['image']
        # check if isbn exists on the databse
        check_book = Book.objects.filter(isbn = isbn)
        if check_book.exists():
            existing = True
            return render(request, 'add_book.html', {'form': form, 'existing': existing})

        books = Book.objects.create(title = title, author = author, isbn = isbn,
            language = language, description = description,
            total_copies = total_copies, book_available = total_copies, image = image)
        books.genre.set(genre_check)
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert': alert, 'form': form})

    return render(request, 'add_book.html', {'form': form})
@login_required
def issue_book(request):
    """This is the one version of issue book"""
    form = forms.IssuedBookForm()
    if not request.user.is_superuser:
        return redirect("/")
    if request.method == "POST":
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            
            alert = True
            return render(request, "issue_book.html", {"obj": obj, 'alert': alert})

    return render(request, "issue_book.html", {'form': form})

@login_required
def issue_book1(request, myid):
    """This is the two version of issue book"""
    if not request.user.is_superuser:
        return redirect("/")
    student = Student.objects.get(id = myid)
    book = Book.objects.all()
    issue_model = IssuedBook1()
    if request.method == "POST":
        book_isbn = str(request.POST['title_isbn']).split("+")
        if len(book_isbn) != 2:
            wrong_data = True
            return render(request, 'issue_book1.html', {'wrong_data': wrong_data, 'student': student, 'book': book})

        title_filter, isbn_filter = book_isbn[0], book_isbn[1]
        book_issue = Book.objects.filter(title = title_filter, isbn = isbn_filter)
        
        if not book_issue.exists():
            nobook= True
            return render(request, 'issue_book1.html', {'nobook': nobook, 'student': student, 'book': book})
        book_final = Book.objects.get(id = book_issue[0].id) # the first query
        issue_model.student = student
        issue_model.book = book_final
        book_final.book_available = book_final.book_available - 1
        book_final.save()
        if book_final.book_available < 1:
            empty = True
            return render(request, 'issue_book1.html', {'empty': empty, 'student': student, 'book': book})
        student.total_books_due += 1
        student.save()
        issue_model.save()
        alert = True
        return render(request, "issue_book1.html", {'alert': alert, 'student': student, 'book': book})
    return render(request, 'issue_book1.html', {'student': student, 'book': book})

@login_required
def issued_book_list(request):
    if not request.user.is_superuser:
        return redirect("/")
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 14:
            day = d - 14
            fine = day * 5
        books = list(models.Book.objects.filter(isbn = i.isbn))
        students = list(models.Student.objects.filter(user = i.student_id))
        j = 0
        for l in books:
            t = (students[j].user, students[j].roll_no, students[j].fullname, 
                books[j].get_slice_title(), books[j].isbn, i.issued_date, i.expiry_date, fine, books[j].id, students[j].id, i.id)
            j += 1
            details.append(t)
    return render(request, 'issued_book_list.html', {'issuedBooks': issuedBooks, 'details': details})

@login_required
def issued_book_list1(request):
    if not request.user.is_superuser:
        return redirect("/")
    issuedBooks = IssuedBook1.objects.all()
    details = []
    j = 0
    for i in issuedBooks:
        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 14:
            day = d - 14
            fine = 5 * day

        books = list(models.Book.objects.filter(id = i.book.id))
        
        students = list(models.Student.objects.filter(id = i.student.id))
        t = (students[j].user, students[j].roll_no, students[j].fullname,
            books[j].get_slice_title(), books[j].isbn, i.issued_date, i.expiry_date, fine, books[j].id, students[j].id, i.id)
        details.append(t)
    return render(request, 'issued_book_list1.html', {'issuedBooks': issuedBooks, 'details': details})

@login_required
def my_issued_book(request):
    if request.user.is_superuser:
        return redirect("/")
    student = Student.objects.filter(user_id = request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id = student[0].user_id)
    li1 = []
    for i in issuedBooks:
        books = Book.objects.filter(isbn = i.isbn)
        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 14:
            day = d - 14
            fine = day * 5
        j = 0
        for book in books:
            t = (request.user.id, request.user.student.fullname, book.get_slice_title(), book.author, issuedBooks[j].issued_date, issuedBooks[j].expiry_date, fine, book.id)
            li1.append(t)
            j += 1
    return render(request, 'my_issued_book.html', {'li1': li1})

@login_required
def my_issued_book1(request):
    if request.user.is_superuser:
        return redirect("/")
    student = Student.objects.get(user_id = request.user.id)
    issuedBooks1 = IssuedBook1.objects.filter(student = student)
    li1 = []
    for i in issuedBooks1:
        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 14:
            day = d - 14
            fine = day * 5
        t = (request.user.id, request.user.student.fullname, i.book.get_slice_title(), i.book.author, i.issued_date, i.expiry_date, fine, i.book.id)
        li1.append(t)
    return render(request, 'my_issued_book1.html', {'li1': li1})

        
def student_login(request):
    if request.user.is_superuser:
        return redirect('/logout')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("<h1>You are not a student.</h1>")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, 'student_login.html', {'alert': alert})
    return render(request, 'student_login.html')


def student_registration(request):
    if request.user.is_superuser:
        return redirect('/logout')
    if request.method == "POST":
        username = request.POST['username']
        #first_name = request.POST['first_name']
        #last_name = request.POST['last_name']
        fullname = request.POST['fullname']
        email = request.POST['email']
        roll_no = request.POST['roll_no']
        classroom = request.POST['classroom']
        branch = request.POST['branch']
        phone = request.POST['phone']
        image = request.FILES['image']

        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            passnotmatch = True
            return render(request, 'student_registration.html', {"passnotmatch": passnotmatch})
        # check if a student with roll_no number that exists in the database
        check_student = Student.objects.filter(roll_no = roll_no)
        if check_student.exists():
            existing = True
            return render(request, 'student_registration.html', {'existing': existing})

        user = User.objects.create_user(username = username, email = email, password = password2)
        student = Student.objects.create(user = user, fullname = fullname, roll_no = roll_no, classroom = classroom,
            branch = branch, phone = phone, image = image)
        user.save()
        student.save()
        alert = True
        return render(request, 'student_registration.html', {'alert': alert})

    return render(request, "student_registration.html")

@login_required
def profile(request):
    if not request.user.is_authenticated:
        redirect("/student_login")
    return render(request, "profile.html")

@login_required
def edit_profile(request):
    if not request.user.is_authenticated:
        redirect("/student_login")
    student = Student.objects.get(user = request.user)
    if request.method == "POST":
        #first_name = request.POST['first_name']
        #last_name = request.POST['last_name']
        fullname = request.POST['fullname']
        email = request.POST['email']
        phone = request.POST['phone']
        roll_no = request.POST['roll_no']
        classroom = request.POST['classroom']
        branch = request.POST['branch']

        #student.user.first_name = first_name
        #student.user.last_name = last_name
        student.user.email = email
        student.fullname = fullname
        student.phone = phone
        student.roll_no = roll_no
        student.classroom = classroom
        student.branch = branch
        student.user.save()
        student.save()
        alert = True
        return render(request, 'edit_profile.html', {'alert': alert})

    return render(request, "edit_profile.html")

@login_required
def edit_book(request, pk):
    if not request.user.is_superuser:
        return redirect("/")
    book = get_object_or_404(Book, id = pk)
    form = forms.BookForm()
    form = forms.BookForm({'genre2': book.genre.get(), 'language2': book.language})
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        genre_check = Genre.objects.filter(genre_name = request.POST['genre2'])
        language_check = Language.objects.get(language_name = request.POST['language2'])
        language = language_check
        description = request.POST['description']
        total_copies = int(request.POST['total_copy'])
        
        #image = request.FILES['image']
        old_quantity_book = book.total_copies # check if adding the number of books is eligible
        book_available = book.book_available
        if total_copies < old_quantity_book - book_available:
            wrong = True
            return render(request, 'edit_book.html', {'form': form, 'book': book, 'wrong': wrong})
        
        book.total_copies = total_copies
        book.book_available = total_copies - (old_quantity_book - book_available)

        book.title = title
        book.author = author
        book.isbn = isbn
        book.language = language
        book.description = description
        
        #if image != "" or image is None:
            #book.image = image
        book.genre.set(genre_check)
        book.save()
        alert = True
        return render(request, 'edit_book.html', {'alert': alert, 'form': form, 'book': book})
    return render(request, 'edit_book.html', {'form': form, 'book': book})

@login_required
def change_password(request):
    if request.method == 'POST':
        curr_password = request.POST['current_password']
        new_password = request.POST['password']
        try:
            user = User.objects.get(id = request.user.id)
            if user.check_password(curr_password):
                user.set_password(new_password)
                user.save()
                alert = True
                return render(request, "change_password.html", {'alert': alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {"currpasswrong": currpasswrong})
        except:
            pass
    return render(request, 'change_password.html')

def book_detail(request, pk):
    book = get_object_or_404(Book, id = pk)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def student_detail(request, pk):
    if not request.user.is_superuser:
        return redirect("/")
    student = get_object_or_404(Student, id = pk)
    return render(request, 'student_detail.html', {'student': student})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_products(request):
    books = Book.objects.all()
    return render(request, 'book_products.html', {'books': books})
    
@login_required
def student_list(request):
    if not request.user.is_superuser:
        return redirect("/")
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def Logout(request):
    logout(request)
    return redirect("/")

@login_required
def delete_book(request, myid):
    if not request.user.is_superuser:
        return redirect("/")
    books = Book.objects.filter(id = myid)
    books.delete()
    return redirect("/book_list")

@login_required
def delete_student(request, myid):
    if not request.user.is_superuser:
        return redirect("/")
    students = Student.objects.get(id = myid)
    if students.total_books_due > 0:
        on_borrow = True
        return render(request, 'student_list.html', {'on_borrow': on_borrow})

    students.delete()
    return redirect("/student_list")

@login_required
def delete_issue(request, myid):
    if not request.user.is_superuser:
        return redirect("/")
    issue = IssuedBook.objects.filter(id = myid)
    issue.delete()
    return redirect("/issued_book_list")

@login_required
def delete_issue1(request, myid):
    if not request.user.is_superuser:
        return redirect("/")
    issue = IssuedBook1.objects.get(id = myid)
    student = Student.objects.get(id = issue.student.id)
    book = Book.objects.get(id = issue.book.id)
    book.book_available = int(book.book_available) + 1
    student.total_books_due = int(student.total_books_due) - 1
    student.save()
    book.save()
    issue.delete()
    return redirect("/issued_book_list1")

# for search book
def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in individual keywords, getting rid of unecessary
    spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.'''
    query = None # Query search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'description', 'author'])
        book_list = Book.objects.filter(entry_query)
    
    return render(request, 'book_products.html', {'books': book_list})

