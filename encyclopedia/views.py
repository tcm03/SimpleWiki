from django.shortcuts import render, redirect
from .forms import NewPageForm
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page_content = util.get_entry(title)
    if page_content is None:
        return render(request, "encyclopedia/error.html", {
            "title": title + " not found",
            "message": "The requested page was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": page_content
        })
    
def search(request):
    query_str = request.GET.get('q')
    entries = util.list_entries()
    if query_str in entries:
        return redirect('encyclopedia:entry', title=query_str)
    else:
        # find those entries that contain the query string as a substring
        results = [entr for entr in entries if query_str.lower() in entr.lower()]
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query_str
        })

def create_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/error.html", {
                    "title": title,
                    'message': 'An wiki page with this title already exists.'
                })
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('encyclopedia:entry', title=title)
    else:
        return render(request, "encyclopedia/create_page.html", {
            "form": NewPageForm()
        })
    
def edit_page(request, title):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('encyclopedia:entry', title=title)
    else:
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "form": NewPageForm(initial={'title': title, 'content': util.get_entry(title)}, read_only_title=True),
        })
    
def random_page(request):
    entries = util.list_entries()
    return redirect('encyclopedia:entry', title=random.choice(entries))