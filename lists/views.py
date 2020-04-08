from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item


# Create your views here.
def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']  # gets posted item from form
        Item.objects.create(text=new_item_text)  # .objects.create is shorthand for creating new item/no need for save()
        return redirect('/')

    items = Item.objects.all()

    return render(request, 'home.html', {'items': items})


