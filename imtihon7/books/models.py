from django.db import models
from django.conf import settings
from shared.models import BaseModel

class Section(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(BaseModel):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='ebooks/', blank=True, null=True)
    
    total_copies = models.PositiveIntegerField(default=1, help_text="Kutubxonadagi jami nusxalar soni")
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class BookReview(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_user_book_review')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}★)"

class BookLike(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_user_book_like')
        ]
        
    def __str__(self):
        return f"{self.user.username} ♥ {self.book.title}"
