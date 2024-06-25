from datetime import datetime
from django.db import models
from django.forms import ValidationError

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    borrow_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=100)
    year_of_publication = models.IntegerField()
    category_name = models.CharField(max_length=100)
    number_of_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.number_of_copies < 0:
            raise ValidationError("The number of copies cannot be negative.")
        super(Book, self).save(*args, **kwargs)


class BorrowRecord(models.Model):
    borrow_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)
    borrow_count = models.PositiveIntegerField(default=1)  # Default value is 1

    def __str__(self):
        return f"{self.user.first_name} borrowed {self.book.title}"



class Suggestion(models.Model):
    suggestion_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    suggested_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author} suggested by {self.user.username}"

class Fine(models.Model):
    fine_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    fine_date = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} has a fine of {self.amount}"
