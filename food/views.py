from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse

from .forms import ItemForm
from .models import Item, Rating
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


class IndexClassView(ListView):
    model = Item
    template_name = 'food/index.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by', 'rating')  # Default to sorting by rating
        if sort_by == 'rating':
            queryset = sorted(queryset, key=lambda x: x.average_rating(), reverse=True)
        elif sort_by == 'views':
            queryset = queryset.order_by('-views')
        return queryset


def item(request):
    return HttpResponse("This is an item view")


class FoodDetail(DetailView):
    model = Item
    template_name = 'food/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj


class CreateItem(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'food/item-form.html'

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)


@login_required
def update_item(request, item_id):
    item = Item.objects.get(id=item_id)

    # Check if the current user is the owner of the item
    if request.user != item.user_name:
        return HttpResponseForbidden("You are not authorized to update this item.")

    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect("food:index")

    return render(request, 'food/item-form.html', {'form': form, 'item_id': item_id})


@login_required
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)

    # Check if the current user is the owner of the item
    if request.user != item.user_name:
        return HttpResponseForbidden("You are not authorized to delete this item.")

    if request.method == 'POST':
        item.delete()
        return redirect("food:index")

    return render(request, 'food/item-delete.html', {'item_id': item_id})


def submit_rating(request, pk):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        rating_value = request.POST.get('rating')
        item = get_object_or_404(Item, pk=item_id)
        # Create or update the rating
        Rating.objects.update_or_create(user=request.user, item=item, defaults={'value': rating_value})
        return redirect('food:detail', pk=pk)
    else:
        # Handle other HTTP methods if needed
        return HttpResponseNotAllowed(['POST'])


def handler404(request, exception):
    return render(request, 'food/404.html', status=404)


def handler500(request):
    return render(request, 'food/500.html', status=500)
