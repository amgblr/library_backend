from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import User,Book
from .serializers import UserSerializer, LoginSerializer

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
            genre=data.get('genre'),
            number_of_copies=data.get('number_of_copies')
        )
        book_data = {
            'book_id': book.book_id,
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'year_of_publication': book.year_of_publication,
            'genre': book.genre,
            'number_of_copies': book.number_of_copies
        }
        return Response(book_data, status=status.HTTP_201_CREATED)

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        book_list = [{
            'book_id': book.book_id,
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'year_of_publication': book.year_of_publication,
            'genre': book.genre,
            'number_of_copies': book.number_of_copies
        } for book in books]
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
            'genre': book.genre,
            'number_of_copies': book.number_of_copies
        }
        return Response(book_data, status=status.HTTP_200_OK)
    
    