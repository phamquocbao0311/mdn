from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Author, Gerne, Book, BookInstance


class BookInline(admin.TabularInline):
    model = Book


# define admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

# admin.site.register(Book)


# Register admin class with model
admin.site.register(Author, AuthorAdmin)
admin.site.register(Gerne)
# admin.site.register(BookInstance)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'display_genre')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstaceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('id', 'book', 'imprint', 'due_back', 'borrower')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


