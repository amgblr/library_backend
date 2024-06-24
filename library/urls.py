from django.urls import path
from .views import AddBookView, BookListView, CreateUserView, DeleteBookCopyView, LoginUserView,AddBookCopyView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('add-book/', AddBookView.as_view(), name='add_book'),
    path('add-book-copy/', AddBookCopyView.as_view(), name='add_book_copy'),
    path('delete-book-copy/', DeleteBookCopyView.as_view(), name='delete_book_copy'),
    
]
