from django.shortcuts import render, redirect
import  markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    entry = util.get_entry(title)
    if entry == None:
        entry = "## Page Not Found!!!" 

    return render(request, "encyclopedia/article.html", {
        "entry": markdown2.markdown(entry),
    }) 

def search(request):
    query = request.GET.get("q").strip()
    if query in util.list_entries():
        return redirect("article", title = query)
    
    return render(request, "encyclopedia/search.html", {
    "entries": util.find_entry(query)
    })