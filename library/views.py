from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Fine, User,Book,BorrowRecord,Category, Suggestion
from .serializers import UserSerializer, LoginSerializer,  BorrowRecordSerializer
from django.db.models import Q
from rest_framework import status
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from django.db.models import F

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

            if check_password(serializer.validated_data['password'], user.password):
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddBookView(generics.CreateAPIView):
    queryset = Book.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        isbn = data.get('isbn')
        
        if Book.objects.filter(isbn=isbn).exists():
            return Response({'detail': 'Book already exists'}, status=300)

        book = Book.objects.create(
            isbn=isbn,
            title=data.get('title'),
            author=data.get('author'),
            publisher=data.get('publisher'),
            year_of_publication=data.get('year_of_publication'),
            category_name=data.get('category_name'),
            number_of_copies=data.get('number_of_copies')
        )
        book_data = {
            'book_id': book.book_id,
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'year_of_publication': book.year_of_publication,
            'category_name': book.category_name,
            'number_of_copies': book.number_of_copies
        }
        return Response(book_data, status=status.HTTP_201_CREATED)

class BookListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        books = Book.objects.filter(number_of_copies__gt=0)
        book_list = []
        for book in books:
            book_list.append({
                'book_id': book.book_id,
                'isbn': book.isbn,
                'title': book.title,
                'author': book.author,
                'publisher': book.publisher,
                'year_of_publication': book.year_of_publication,
                'category_name': book.category_name,
                'number_of_copies': book.number_of_copies
            })
        return Response(book_list, status=status.HTTP_200_OK)  

class AddBookCopyView(APIView):
    def put(self, request, *args, **kwargs):
        isbn = request.data.get('isbn')
        copies_to_add = int(request.data.get('copies', 0))

        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        book.number_of_copies += copies_to_add
        book.save()

        book_data = {
            'book_id': book.book_id,
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'year_of_publication': book.year_of_publication,
            'category_name': book.category_name,
            'number_of_copies': book.number_of_copies
        }
        return Response(book_data, status=status.HTTP_200_OK)
    
class DeleteBookCopyView(APIView):
    def put(self, request, *args, **kwargs):
        isbn = request.data.get('isbn')
        copies_to_delete = int(request.data.get('copies', 0))

        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        if book.number_of_copies < copies_to_delete:
            return Response({'detail': 'Not enough copies to delete'}, status=status.HTTP_400_BAD_REQUEST)

        book.number_of_copies -= copies_to_delete
        book.save()

        book_data = {
            'book_id': book.book_id,
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'year_of_publication': book.year_of_publication,
            'category_name': book.category_name,
            'number_of_copies': book.number_of_copies
        }
        return Response(book_data, status=status.HTTP_200_OK)
    
# class SearchBooksView(APIView):
#     def get(self, request, *args, **kwargs):
#         query = request.GET.get('q', '')

#         if not query:
#             return Response({'detail': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

#         books = Book.objects.filter(
#             Q(title__icontains=query) |
#             Q(author__icontains=query) |
#             Q(publisher__icontains=query) |
#             Q(category_name__icontains=query) |
#             Q(isbn__icontains=query)
#         )

#         book_list = [{
#             'book_id': book.book_id,
#             'isbn': book.isbn,
#             'title': book.title,
#             'author': book.author,
#             'publisher': book.publisher,
#             'year_of_publication': book.year_of_publication,
#             'category_name': book.category_name,
#             'number_of_copies': book.number_of_copies
#         } for book in books]

#         return Response(book_list, status=status.HTTP_200_OK)

class DeleteBookView(APIView):
    def delete(self, request, isbn):
        try:
            book = Book.objects.get(isbn=isbn)
            book.delete()
            return Response({"message": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

class SearchBooksByCategoryView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        category_name = request.query_params.get('category_name', None)
        if category_name:
            books = Book.objects.filter(category_name=category_name, number_of_copies__gt=0)
            if books.exists():
                book_list = [{
                    'book_id': book.book_id,
                    'isbn': book.isbn,
                    'title': book.title,
                    'author': book.author,
                    'publisher': book.publisher,
                    'year_of_publication': book.year_of_publication,
                    'category_name': book.category_name,
                    'number_of_copies': book.number_of_copies
                } for book in books]
                return Response(book_list, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'No books found for the given category name'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'Category name parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
class AddCategoryView(APIView):
    def post(self, request):
        category_name = request.data.get('category_name')
        if category_name:
            category, created = Category.objects.get_or_create(category_name=category_name)
            if created:
                return Response({"message": "Category added successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Category already exists."}, status=status.HTTP_200_OK)
        return Response({"error": "Category name is required."}, status=status.HTTP_400_BAD_REQUEST)
    
class BorrowBookView(generics.CreateAPIView):
    queryset = BorrowRecord.objects.all()

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=7)  # Due date is 7 days from borrow date

        # Validate the user and book
        user = get_object_or_404(User, pk=user_id)
        book = get_object_or_404(Book, pk=book_id)

        # Check if the user has already borrowed four books
        if user.borrow_count >= 4:
            return Response({'detail': 'User has already borrowed four books'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the book is available for borrowing
        if book.number_of_copies > 0:
            # Create the borrow record
            borrow_record = BorrowRecord.objects.create(
                user=user,
                book=book,
                borrow_date=borrow_date,
                due_date=due_date
            )
            # Decrement the number of copies
            book.number_of_copies -= 1
            book.save()

            # Increment the borrow count of the user
            User.objects.filter(pk=user_id).update(borrow_count=F('borrow_count') + 1)

            borrow_data = {
                'borrow_id': borrow_record.borrow_id,
                'user_id': borrow_record.user.user_id,
                'book_id': borrow_record.book.book_id,
                'book_name': borrow_record.book.title,  # Include book name
                'borrow_date': borrow_record.borrow_date,
                'due_date': borrow_record.due_date,
                'return_date': borrow_record.return_date
            }
            return Response(borrow_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'No copies of the book are available for borrowing'}, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')

        # Validate the user and book
        user = User.objects.filter(user_id=user_id).first()
        book = Book.objects.filter(book_id=book_id).first()

        if not user or not book:
            return Response({'detail': 'User or Book not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has borrowed the book
        borrow_record = BorrowRecord.objects.filter(user=user, book=book, returned=False).first()
        if not borrow_record:
            return Response({'detail': 'User has not borrowed this book'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the book as returned
        borrow_record.returned = True
        borrow_record.return_date = date.today()
        borrow_record.save()

        # Increment the number of copies of the book
        book.number_of_copies += 1
        book.save()

        return Response({'detail': 'Book returned successfully'}, status=status.HTTP_200_OK)

class UserBorrowedBooksView(generics.ListAPIView):
    serializer_class = BorrowRecordSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(pk=user_id)
        return BorrowRecord.objects.filter(user=user, returned=False)

class SuggestBook(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if Suggestion.objects.filter(user=user, suggested_date__month=date.today().month).exists():
            return Response({"error": "You have already suggested a book this month"}, status=status.HTTP_400_BAD_REQUEST)
        
        title = request.data.get('title')
        author = request.data.get('author')
        
        suggestion = Suggestion(user=user, title=title, author=author)
        suggestion.save()
        
        return Response({"message": "Book suggested successfully"}, status=status.HTTP_201_CREATED)

class CalculateFine(APIView):
    def get(self, request, user_id):
        # Get the user object
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Calculate total fine for the user
        total_fine = 0
        borrow_records = BorrowRecord.objects.filter(user=user, returned=True).exclude(return_date__gte=date.today())
        for record in borrow_records:
            due_date = record.due_date
            return_date = record.return_date
            if return_date is None:
                return_date = date.today()
            days_diff = (return_date - due_date).days
            fine_amount = days_diff * 5
            total_fine += fine_amount

        return Response({"user_id": user_id, "total_fine": total_fine}, status=status.HTTP_200_OK)
    
    def post(self, request, user_id):
        # Get the user object
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Calculate total fine for the user
        total_fine = 0
        borrow_records = BorrowRecord.objects.filter(user=user, returned=True).exclude(return_date__gte=date.today())
        for record in borrow_records:
            due_date = record.due_date
            return_date = record.return_date
            if return_date is None:
                return_date = date.today()
            days_diff = (return_date - due_date).days
            fine_amount = days_diff * 5
            total_fine += fine_amount

        # Save the fine record
        fine = Fine.objects.create(
            user=user,
            amount=total_fine,
            reason="Late return of books",
            fine_date=date.today()
        )

        return Response({"message": "Fine calculated and saved successfully", "fine_id": fine.fine_id}, status=status.HTTP_201_CREATED)












