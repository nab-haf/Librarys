from django.contrib import admin
from .models import Category,Author,Book,Member,Borrowing

# Register your models here.
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Member)
# admin.site.register(Bookcop)
admin.site.register(Borrowing)