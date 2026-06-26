from django.contrib import admin
from .models import Section, Author, Book, BookReview, BookLike

admin.site.register(Section)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookReview)
admin.site.register(BookLike)
