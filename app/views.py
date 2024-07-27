from django.views import generic
from app.models import Book, Author, Log
from app.form import AuthorForm, BookForm, LogForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
import requests
import json
import time

class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'book_list'
    queryset = Book.objects.all()

def bookdetail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    systemid = "Tokyo_Shinagawa"
    endpoint = "https://api.calil.jp/check"
    headers={

    }
    params={
        "appkey":"424cc27777b9eb2f84d99bcc659d790b",
        "isbn":book.isbn,
        "systemid":systemid
    }

    result = requests.get(endpoint, headers=headers, params=params)
    rjson = result.text.lstrip("callback(").rstrip(");")
    rjson = '{"data":' + rjson + "}"
    data=json.loads(rjson)

    session = data.get('data', {}).get('session', '')

    system_data = data.get('data', {}).get('books', {}).get(str(book.isbn),{}).get(systemid, {})
    library_data = system_data.get('libkey', {})
    status = system_data.get('status', "Error")

    return render(request, 'app/detail.html', {
        'book': book, 'library': library_data, 'session': session, 'status': status
        })

def requestlibrarydata(request, pk):
    if request.method == "POST":
        book = get_object_or_404(Book, pk=pk)
        session = request.POST.get('session')

        endpoint = "https://api.calil.jp/check"
        headers = {}
        params = {
            "appkey": "424cc27777b9eb2f84d99bcc659d790b",
            "session": session
        }
        result = requests.get(endpoint, headers=headers, params=params)
        rjson = result.text.lstrip("callback(").rstrip(");")
        rjson = '{"data":' + rjson + "}"
        data=json.loads(rjson)
        system_data = data.get('data', {}).get('books', {}).get(str(book.isbn),{}).get('Tokyo_Shinagawa', {})
        library_data = system_data.get('libkey', {})

        return redirect('app:book_detail', pk=pk)
    
    return redirect('app:book_detail', pk=pk)




class RegisterAuthorView(generic.CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'app/register.html'
    def get_success_url(self):
        return reverse('app:registerbook')
    
class RegisterBookView(generic.CreateView):
    model = Book
    form_class = BookForm
    template_name = 'app/register.html'
    def get_success_url(self):
        return reverse('app:writinglog')
    
class WritingLogView(generic.CreateView):
    model = Log
    form_class = LogForm
    template_name = 'app/register.html'
    def get_success_url(self):
        return reverse('app:book_detail', kwargs={'pk': self.object.book.pk})

class UpdateLogView(generic.UpdateView):
    model = Log
    form_class = LogForm
    template_name = "app/register.html"
    def get_success_url(self):
        return reverse('app:book_detail', kwargs={'pk': self.object.book.pk})
    
class UpdateBookView(generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = "app/register.html"
    def get_success_url(self):
        return reverse('app:book_detail', kwargs={'pk': self.object.pk})

def deletelog(request, pk):
    obj = get_object_or_404(Log, id=pk)
    book_id = obj.book.pk
    if request.method == "POST":
        obj.delete()
        return redirect('app:book_detail', pk=book_id)
    context = {'obj':obj}
    return render(request, "app/delete.html", context)

def deletebook(request, pk):
    obj = get_object_or_404(Book, id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('app:index')
    context = {'obj':obj}
    return render(request, "app/delete.html", context)

def writingthisbooklog(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = LogForm({'book':book})

    if request.method == "GET":
        form = LogForm(initial={'book':book})
        return render(request, 'app/register.html', {'form': form})
 
    if request.method == "POST":
        form = LogForm(request.POST)
        if form.is_valid():
            l = form.save(commit=False)
            l.book = book
            l.save()
            return redirect('app:book_detail', pk=l.book.pk)
        else:
            return render(request, 'app/register.html', {'form': form})
