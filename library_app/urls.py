from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("admin_login/", views.admin_login, name = "admin_login"),
    path("add_book/", views.add_book, name = "add_book"),
    path("issue_book/", views.issue_book, name = "issue_book"),
    path("issued_book_list/", views.issued_book_list, name = "issued_book_list"),
    path("issued_book_list1/", views.issued_book_list1, name = "issued_book_list1"),

    path('issue_book1/<int:myid>/', views.issue_book1, name = 'issue_book1'),

    path("book_list/", views.book_list, name = "book_list"),
    path("book_products/", views.book_products, name = 'book_products'),
    path('book/<int:pk>/', views.book_detail, name = 'book_detail'),
    path('edit_book/<int:pk>/', views.edit_book, name = 'edit_book'),

    path('student_list/', views.student_list, name = 'student_list'),
    path('student/<int:pk>/', views.student_detail, name = "student_detail"),

    path("student_login/", views.student_login, name = "student_login"),
    path("student_registration/", views.student_registration, name = "student_registration"),
    path("profile/", views.profile, name = "profile"),
    path("edit_profile/", views.edit_profile, name = "edit_profile"),
    path("my_issued_book/", views.my_issued_book, name = "my_issued_book"),
    path("my_issued_book1/", views.my_issued_book1, name = 'my_issued_book1'),
    
    path("change_password/", views.change_password, name = "change_password"),

    path("logout/", views.Logout, name = "logout"),

    path("delete_book/<int:myid>/", views.delete_book, name = "delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name = "delete_student"),
    path("delete_issue/<int:myid>/", views.delete_issue, name = "delete_issue"),
    path("delete_issue1/<int:myid>/", views.delete_issue1, name = 'delete_issue1'),
    
    url(r'^search_b/', views.search_book, name = 'search_b'),

]