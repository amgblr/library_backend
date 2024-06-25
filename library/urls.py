from django.urls import path
from .views import AddBookView, AddCategoryView, BookListView, BorrowBookView, CalculateFine, CreateUserView, DeleteBookCopyView, DeleteBookView, LoginUserView,AddBookCopyView, ReturnBookView, SearchBooksByCategoryView
from .views import UserBorrowedBooksView,SuggestBook
urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('add-book/', AddBookView.as_view(), name='add_book'),
    path('add-book-copy/', AddBookCopyView.as_view(), name='add_book_copy'),
    path('delete-book-copy/', DeleteBookCopyView.as_view(), name='delete_book_copy'),
    # path('search-books/', SearchBooksView.as_view(), name='search_books'),
    path('delete-book/<str:isbn>/', DeleteBookView.as_view(), name='delete_book'),
    # path('search-books-by-category/<str:category_name>/', SearchBooksByCategoryView.as_view(), name='search_books_by_category'),
    path('add-category/', AddCategoryView.as_view(), name='add_category'),
    path('search-books/', SearchBooksByCategoryView.as_view(), name='search_books_by_category'),
    path('borrow-book/', BorrowBookView.as_view(), name='borrow_book'),
    path('return-book/', ReturnBookView.as_view(), name='return_book'),
    path('borrowed-books/<int:user_id>/', UserBorrowedBooksView.as_view(), name='user_borrowed_books'),
    path('suggest-book/', SuggestBook.as_view(), name='suggest_book'),
    path('calculate-fine/<int:user_id>/', CalculateFine.as_view(), name='calculate-fine'),



]
    

