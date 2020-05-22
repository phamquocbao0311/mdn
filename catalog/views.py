from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Gerne
from django.shortcuts import get_object_or_404, Http404
from django.contrib.auth.mixins import LoginRequiredMixin


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

    #session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_gerne,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book

    def get_queryset(self):
        return Book.objects.all() # Get 5 books containing the title war


class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(generic.ListView):
    model = Author

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailView(generic.DetailView):

    model = Author

    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'catalog/author_detail.html', context={'author': author})

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class UserManageLoanedBookListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower__isnull=False)
