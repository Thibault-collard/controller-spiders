from distutils.log import error
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm
from spider_app import run_spider

def post_form(request):
    
    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:

        form = NameForm(request.POST or None)
        # check whether it's valid:
        if form.is_valid():
            run_spider.RunSpider(form.cleaned_data)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')
        else:
            print(form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'form.html', {'form': form})

