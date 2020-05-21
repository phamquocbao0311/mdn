from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Gerne
from django.shortcuts import get_object_or_404, Http404


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_gerne = Gerne.objects.all().count()
    # num_gerne_available = Gerne.objects.filter(status__exact='a').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_gerne,
        # 'num_gerne_available': num_gerne_available,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book

    def get_queryset(self):
        return Book.objects.all()[:5]  # Get 5 books containing the title war

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        print(type(book))
        return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    model = Author

    def get_queryset(self):
        return Author.objects.all()

class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view( request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        books = Book.objects.filter(author_id=primary_key)
        return render(request, 'catalog/author_detail.html', context={'author': author,'books': books})