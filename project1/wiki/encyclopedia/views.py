from django.shortcuts import render, redirect
import  markdown2
from . import util
from django import forms
from django.urls import reverse
import re

class NewPageForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Page Title"})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter Page Content in Markdown format"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    entry = util.get_entry(title)
    if entry == None:
        entry = "## Page Not Found!!!" 
    # entry = re.sub(r'\[(.*?)\]\(/wiki/([^)]+)\)', r'[\1](/\2)', entry)
    return render(request, "encyclopedia/article.html", {
        "entry": markdown2.markdown(entry),
        "title": title
    }) 

def search(request):
    query = request.GET.get("q").strip()
    if query in util.list_entries():
        return redirect("article", title = query)
    
    return render(request, "encyclopedia/search.html", {
    "entries": util.find_entry(query)
    })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            'new_page': NewPageForm()
        })
    elif request.method == "POST":
        data = NewPageForm(request.POST)
        if data.is_valid():
            title = data.cleaned_data['title'].strip()
            content = data.cleaned_data['content'].strip()
            if title not in util.list_entries():
                util.save_entry(title, content)
                return redirect("article", title = title)
            else:
                title_url = reverse('article', args=[title])
                error_message = f"The page you are trying to create already exists here - [{title}]({title_url})."
                return render(request, "encyclopedia/create.html", {
                    'new_page': NewPageForm(),
                    'message' : markdown2.markdown(error_message),
                    'title_url': title_url
                 })
        else:
            error_message = "Entry is not valid"
            return render(request, "encyclopedia/create.html", {
                    'new_page': NewPageForm(),
                    'message' : markdown2.markdown(error_message)
                 })
def edit(request, title):
    if request.method == "GET":
        entry = util.get_entry(title)
        content = re.sub(r'^# .*', '', entry, flags=re.MULTILINE)
        unedited = {
            'title': title,
            'content': entry
        }
        return render(request, "encyclopedia/edit.html", {
            'new_page': NewPageForm(unedited),
            'title': title,
            'content': entry
        }) 
    elif request.method == "POST":
        data = NewPageForm(request.POST)
        
        if data.is_valid():
            title = data.cleaned_data['title'].strip()
            content = data.cleaned_data['content'].strip()
            util.save_entry(title, content)
            return redirect("article", title = title)
        else:
            error_message = "Entry is not valid"
            return render(request, "encyclopedia/article.html", {
                    'title':title,
                    'message' : markdown2.markdown(error_message)
                 })

    