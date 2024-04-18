from django.http import HttpResponse
from django.shortcuts import render
from .models import Item
from django.template import loader


# Create your views here.

def index(request):
    item_list = Item.objects.all()
    template = loader.get_template('food/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def item(request):
    return HttpResponse("This is an item view")