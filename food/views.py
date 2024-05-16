from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ItemForm, CommentForm
from .models import Item, Comment
from star_ratings.models import Rating


class IndexClassView(ListView):
    model = Item
    template_name = 'food/index.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by', 'rating')
        if sort_by == 'rating':
            queryset = sorted(queryset, key=lambda x: x.get_average_rating(), reverse=True)
        elif sort_by == 'views':
            queryset = queryset.order_by('-views')
        return queryset


class FoodDetail(DetailView):
    model = Item
    template_name = 'food/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class CreateItem(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'food/item-form.html'
    success_url = reverse_lazy('food:index')

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)


class UpdateItem(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'food/item-form.html'
    success_url = reverse_lazy('food:index')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user_name != self.request.user:
            raise HttpResponseForbidden("You are not authorized to update this item.")
        return obj


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'food/item-delete.html'
    success_url = reverse_lazy('food:index')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user_name != self.request.user:
            raise HttpResponseForbidden("You are not authorized to delete this item.")
        return obj


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.item = get_object_or_404(Item, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('food:detail', kwargs={'pk': self.kwargs['pk']})


@login_required
def delete_comment(request, item_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, item_id=item_pk)
    if request.user == comment.user or request.user == comment.item.user_name:
        comment.delete()
        return redirect('food:detail', pk=item_pk)
    else:
        return HttpResponseForbidden("You are not authorized to delete this comment.")


def submit_rating(request, pk):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        rating_value = request.POST.get('rating')
        item = get_object_or_404(Item, pk=item_id)
        # Create or update the rating
        Rating.objects.update_or_create(user=request.user, content_object=item, defaults={'score': rating_value})
        return redirect('food:detail', pk=pk)
    else:
        return HttpResponseNotAllowed(['POST'])


def handler404(request, exception):
    return render(request, 'food/404.html', status=404)


def handler500(request):
    return render(request, 'food/500.html', status=500)
