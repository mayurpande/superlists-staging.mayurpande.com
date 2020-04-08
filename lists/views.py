from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item


# Create your views here.
def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']  # gets posted item from form
        Item.objects.create(text=new_item_text)  # .objects.create is shorthand for creating new item/no need for save()
        return redirect('/lists/the-only-list-in-the-world')

    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()

    return render(request, 'list.html', {'items': items})


