from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, JsonResponse, \
    HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ItemForm, CommentForm
from .models import Item, Comment
from star_ratings.models import Rating, UserRating
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


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


# @login_required
# def delete_comment(request, item_pk, comment_pk):
#     comment = get_object_or_404(Comment, pk=comment_pk, item_id=item_pk)
#     if request.user == comment.user or request.user == comment.item.user_name:
#         comment.delete()
#         return redirect('food:detail', pk=item_pk)
#     else:
#         return HttpResponseForbidden("You are not authorized to delete this comment.")


# def submit_rating(request, pk):
#     if request.method == 'POST':
#         item_id = request.POST.get('item_id')
#         rating_value = request.POST.get('rating')
#         item = get_object_or_404(Item, pk=item_id)
#         # Create or update the rating
#         Rating.objects.update_or_create(user=request.user, content_object=item, defaults={'score': rating_value})
#         return redirect('food:detail', pk=pk)
#     else:
#         return HttpResponseNotAllowed(['POST'])

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'food/comment_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        item_pk = self.kwargs['item_pk']
        return reverse_lazy('food:detail', kwargs={'pk': item_pk})

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if self.request.user != comment.user and self.request.user != comment.item.user_name:
            raise HttpResponseForbidden("You are not authorized to delete this comment.")
        return comment


def handle_rating_submission(user, pk, rating_value):
    item = get_object_or_404(Item, pk=pk)
    content_type = ContentType.objects.get_for_model(Item)

    rating, created = Rating.objects.get_or_create(
        content_type=content_type,
        object_id=item.id,
    )

    user_rating, created = UserRating.objects.update_or_create(
        user=user,
        rating=rating,
        defaults={'score': rating_value}
    )
    return {'success': 'Rating submitted successfully'}


class SubmitRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            rating_value = request.data.get('rating')
            if rating_value is None:
                return Response({'error': 'Rating value is required'}, status=status.HTTP_400_BAD_REQUEST)

            result = handle_rating_submission(request.user, pk, rating_value)
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def submit_rating(request, pk):
#     if request.method == 'POST':
#         try:
#             print(f"Received request to rate item with ID: {pk}")
#             item = get_object_or_404(Item, pk=pk)
#             rating_value = request.data.get('rating')
#             print(f"Rating value received: {rating_value}")
#             if rating_value is None:
#                 return JsonResponse({'error': 'Rating value is required'}, status=400)
#
#             # Update or create the user rating
#             user_rating, created = UserRating.objects.update_or_create(
#                 user=request.user,
#                 rating=item.rating,
#                 defaults={'score': rating_value}
#             )
#             return JsonResponse({'success': 'Rating submitted successfully'})
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return HttpResponseNotAllowed(['POST'])


def handler404(request, exception):
    return render(request, 'food/404.html', status=404)


def handler500(request):
    return render(request, 'food/500.html', status=500)
